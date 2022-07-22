import re

from users.models import User

def check_username(username):
    REGEX_USERNAME = "^[A-Za-z0-9]{4,12}$"
    if not re.match(REGEX_USERNAME, username):
        raise ValueError("INVALID_USERNAME_FORMAT")

def check_password(password):
    REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
    if not re.match(REGEX_PASSWORD, password):
        raise ValueError("INVALID_PASSWORD_FORMAT")

def check_email(email):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(REGEX_EMAIL, email):
        raise ValueError("INVALID_EMAIL_FORMAT")

def check_phone_number(phone_number):
    REGEX_PHONE_NUMBER = '^\d{3}-\d{3,4}-\d{4}$'
    if not re.match(REGEX_PHONE_NUMBER, phone_number ):
        raise ValueError("INVALID_PHONE_NUMBER_FORMAT")

def duplicate_check_username(username):
    if User.objects.filter(username = username).exists():
        raise ValueError("INVILD_USERNAME")

def duplicate_check_email(email):
    if User.objects.filter(email = email).exists():
        raise ValueError("INVAILD_EMAIL")

def duplicate_check_phone_number(phone_number):
    if User.objects.filter(phone_number = phone_number).exists():
        raise ValueError("INVAILD_PHONE_NUMBER")