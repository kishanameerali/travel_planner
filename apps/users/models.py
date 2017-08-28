from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = []
        #to check if email already has been registered
        if self.filter(email=postData['email']):
            errors.append("Email has already been registered")
        #to check if alias is already taken
        if self.filter(email=postData['username']):
            errors.append("That Username is already in use")
        if len(postData['name']) < 3:
            errors.append("Name must be 3 characters minimum")
        if len(postData['username']) < 3:
            errors.append("Username must be 3 characters minimum")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid Email Address")
        if len(postData['password']) < 8:
            errors.append("Password must be 8 chracters minimum")
        if postData['password'] != postData['confirm_password']:
            errors.append("Password and confirmation don't match")
        return errors

    def create_user(self, clean_data):
        hashed_pw = bcrypt.hashpw(clean_data['password'].encode(), bcrypt.gensalt())
        return self.create(
            name = clean_data['name'],
            username = clean_data['username'],
            email = clean_data['email'],
            password = hashed_pw
        )

    def login_validator(self, postData):
        #returns tuple ([errors], <User> or None)
        errors = []
        user_login = None
        if not self.filter(email=postData['email']):
            errors.append("Email or Password Invalid")
        else:
            user_login = self.get(email=postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), user_login.password.encode()):
                errors.append("Email or Password Invalid")
                user_login = None
        return (errors, user_login)

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return "Name: {}, Username: {}, Email: {}".format(self.name, self.username, self.email)

