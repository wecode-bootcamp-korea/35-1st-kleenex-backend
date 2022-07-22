import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from users.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            name         = data["name"]
            username     = data["username"]
            password     = data["password"]
            address      = data["address"]
            email        = data["email"]
            phone_number = data["phone_number"]

            check_username(username)
            check_password(password)
            check_phone_number(phone_number)
            check_email(email)

            hashed_password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name            = name,
                username        = username,
                password        = hashed_password,
                address         = address,
                email           = email,
                phone_number    = phone_number
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)
        except ValueError as e :
            return JsonResponse({"MESSAGE": f"{e}"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            user             = User.objects.get(username = data['username'])
            hashed_password  = user.password.encode('utf-8')

            if not bcrypt.checkpw(data['password'].encode('utf-8'), hashed_password):
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=400)

            access_token     = jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse(
                {"MESSAGE"      : "LOGIN SUCCESS",
                 "ACCESS_TOKEN" : access_token},
                status= 200
                )

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"},status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE" :"DOESNOTEXIST"}, status=400)

def check_username(username):
    REGEX_USERNAME = "^[A-Za-z0-9]{4,12}$"
    if not User.objects.filter(username = username).exists():
        if not re.compile(REGEX_USERNAME).match(username):
            raise ValueError("INVILD_USERNAME")
    else:
        raise ValueError("EXISTED_USERNAME")

def check_password(password):
    REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
    if not re.compile(REGEX_PASSWORD).match(password):
        raise ValueError("INVAILD_PASSWORD")

def check_email(email):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not User.objects.filter(email = email).exists():
        if not re.compile(REGEX_EMAIL).match(email):
            raise ValueError("INVAILD_EMAIL")
    else:
        raise ValueError("INVAILD_EMAIL")

def check_phone_number(phone_number):
    REGEX_PHONE_NUMBER = '^\d{3}-\d{3,4}-\d{4}$'
    if not User.objects.filter(phone_number = phone_number).exists():
        if not re.compile(REGEX_PHONE_NUMBER).match(phone_number):
            raise ValueError("INVAILD_PHONE_NUMBER")
    else:
        raise ValueError("EXISTED_PHONE_NUMBER")