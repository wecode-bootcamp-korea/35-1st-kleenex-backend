import json
import bcrypt

from django.http import JsonResponse
from django.views import View

from users.models import User
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