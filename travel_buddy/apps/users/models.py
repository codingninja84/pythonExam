from __future__ import unicode_literals
import re, bcrypt
from django.db import models
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, formData):
        #store possbile failed validations
        errors = []
        if len(formData['name']) < 3:
            errors.append("First name must be at least 2 characters long!")
        if len(formData['userName']) < 3:
            errors.append("Last name must be at least 2 characters long!")
        if not len(formData['email']):
            errors.append("email is required")
        if not EMAIL_REGEX.match(formData['email']):
            errors.append("email is not valid")
        if len(formData['password']) < 8:
            errors.append("Password must be 8 char long!")
        if not formData['password'] == formData['confirm']:
            errors.append("Passwords must match")

        userName = User.objects.filter(userName= formData['userName'])
        user = User.objects.filter(email= formData['email'])
        if userName:
            errors.append("Username must be unique!")
        if user:
            errors.append("Username must be unique!")
        response = {}

        if errors:
            response['status'] = False
            response['errors'] = errors
            return response
        else:
            hashedPw = bcrypt.hashpw(formData['password'].encode(), bcrypt.gensalt())
            user = self.create(user=formData['name'], userName=formData['userName'], email=formData['email'], password=hashedPw)
            response['status'] = True
            response['user'] = user
            return response

    def login(self, formData):
        response = {}
        errors = []

        if len(formData['userName']) < 3:
            errors.append("Username required")
        if len(formData['password']) < 8:
            errors.append("Password required")

        else:
            user = User.objects.filter(userName=formData['userName'])
            if user:
                if bcrypt.checkpw(formData['password'].encode(), user[0].password.encode()):
                    response['user'] = user[0]
                    response['status'] = True
                    return response
                else:
                    response['status'] = False
                    response['errors'] = "Invalid Password/Username Combo!"
                    return response
            else:
                errors.append("Invalid Password/Username Combo!")
        response['status'] = False
        response['errors'] = errors
        return response

class User(models.Model):
    user = models.CharField(max_length=38)
    userName = models.CharField(max_length= 38)
    email = models.CharField(max_length= 25)
    password = models.CharField(max_length= 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
