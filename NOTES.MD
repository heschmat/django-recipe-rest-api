```sh
docker build .
docker-compose build

# If you see no output running this, all is well as far as linting is concerned.
docker-compose run --rm app sh -c "flake8"

# To create our django project:
docker-compose run --rm app sh -c "django-admin startproject app ."

docker-compose up # starts our services

# locally you can visit the app at: http://127.0.0.1:3000/
docker-compose run --rm -p 3000:8000 app sh -c "python manage.py runserver 0.0.0.0:8000"
```
