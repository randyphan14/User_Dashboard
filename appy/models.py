from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if postData['first_name'].isalpha():
            errors["first_name"] = "First name should only contain characters"
        if postData['last_name'].isalpha():
            errors["last_name"] = "Last name should only contain characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['password1']:
            errors["password"] = "Password do not match"
        return errors

    def password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['password1']:
            errors["password"] = "Password do not match"
        return errors

    def user_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        # if postData['first_name'].isalpha():
        #     errors["first_name"] = "First name should only contain characters"
        # if postData['last_name'].isalpha():
        #     errors["last_name"] = "Last name should only contain characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors

class User(models.Model):
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.CharField(max_length=255, default = "user")
    desc = models.TextField(default = "")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #message = list of messages the user has written
    #comments = list of comments the user has written
    #walle = list of messages written for the user


class Message(models.Model):
    desc = models.TextField()
    author = models.ForeignKey(User, related_name = "messages", on_delete = models.CASCADE)
    wall_owner = models.ForeignKey(User, related_name = "walle", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #comments = list of comments on message

class Comment(models.Model):
    desc = models.TextField()
    author = models.ForeignKey(User, related_name = "comments", on_delete = models.CASCADE)
    messages = models.ForeignKey(Message, related_name = "messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)