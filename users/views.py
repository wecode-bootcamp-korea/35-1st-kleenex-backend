import bcrypt
import jwt
import json

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from core.utils import *

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
            duplicate_check_username(username)
            duplicate_check_email(email)
            duplicate_check_phone_number(phone_number)

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