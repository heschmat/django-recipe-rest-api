from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Just in case we want to implement this in the future.
from django.utils.translation import gettext_lazy as _   # standard django convention

from . import models


# Register your models here.
class UserAdmin(BaseUserAdmin):
    """Design the admin page for users."""
    ordering = ['id']
    list_display = ['email', 'name']

    # modifications so that `test_edit_user_page` passes: admin/core/user/1/change/
    # Modify `fieldsets` per the fields in our customized `User` model, in models.py
    fields_permissions = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        # (title, {'fields', fields_names_tuple});
        # None means no title for that section.
        (None, {'fields': ('email', 'password')}),
        # Permissions section
        (_('Permissions'), {'fields': fields_permissions}),
        (_('Important Dates'), {'fields': ('last_login',)})
    )

    readonly_fields = ('last_login',)

    # ======================================================================= #
    # for `test_create_user_page()`: admin/core/user/add/
    # The `add_fieldsets` definition should be a tuple
    # containing a section title and a dictionary with a fields key.
    fields_required_new_user = (
        'email',
        'password1',
        'password2',   # password confirmation
        'name',
        'is_active', 'is_staff', 'is_superuser'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),   # just for page desing aspect
            'fields': fields_required_new_user
        }),   # don't forget the comma here
        # otherwise: TypeError: cannot unpack non-iterable NoneType object
    )


# Register User model with our desired modificationss for ordering & display list.
admin.site.register(models.User, UserAdmin)
