# Library_service API
- Api service for library written on DRF

## Feauters:
- JWT authenticated
- Admin panel /admin/
- Documentation is located via /api/doc/swagger/
- Managing your borrowings
- Creating, updating books(Only for staff) 
- Filtering borrowings by users id(Only for staff) and active borrowing
- Notification on telegram when create new borrow
- Notification every day with information about borrowings
- Task control using the flower
- Payment using the Stripe service
- Docker app starts only when db is available ( custom command via management/commands )

## Installing using GitHub:
-Install Postgres and create DB

```shell
git clone https://github.com/bythewaters/library-service.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
open .env.sample and change enviroment variables on yours !Rename file from .env.sample to .env
python manage.py migrate
python manage.py runserver
```
- Use the following command to load prepared data from fixture(if you need):
  - `python manage.py loaddata library_service.json`.

## Defaults users:
```
1. Staff:
  email: admin@admin.com
  password: admin1849

2. Regular user:
  email: test@user.com
  password: testuser1234
  
Also you can create your superuser using command:
python manage.py createsuperuser
```
## Get TELEGRAM_CHAT_ID and connect telegram alerts:
Add the Telegram BOT to your group using name `@MyPythonProjectNot_Bot`

## Connect Stripe Payment:
1. Register on site [stripe.com](https://www.stripe.com)
2. Copy your secret key and set in .env file.

## Run with Docker:
- Docker should be installed
```
- docker-compose build
- docker-compose up
```
- Use the following command to load prepared data from fixture in docker(if you need):
  - `docker ps`(copy name or id docker container)
  - `docker exec -t -i <docker_name_or_id> sh`
  - `python manage.py loaddata library_service_data.json`.

## Getting access:
- Create user via /api/user/register/
- Get user token via /api/user/token/
- Authorize with it on /api/doc/swagger/ OR 
- Install ModHeader extension and create Request header with value ```Bearer <Your access token>```
