# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
    def register_validation(self, postData):
        results = {'errors':[], 'status':True}
        if len(postData['name'])<2 or not postData['name'].isalpha():
           results['status'] = False
           results['errors'] += ["Name must be at least 2 letters"]
        if len(postData['alias'])<2 or not postData['alias'].isalnum():
           results['status'] = False
           results['errors'] += ["Alias must be at least 2 letters or numbers"]
        if not re.match(r'[^@]+@[^@]+\.[^@]+', postData['email']):
            results['status'] = False
            results['errors'] += ["Email is not in a standard email format"]
        if len(postData['password'])<8 or not postData['password'].isalnum():
            results['status'] = False
            results['errors'] += ["Password must have at least 8 characters only comprised of letters and numbers"]
        if postData['password'] != postData['password2']:
            results['status'] = False
            results['errors'] += ["Passwords did not match each other"]
        try:
            user = User.objects.get(email=postData['email'])
            results['status'] = False
            results['errors'] += ["This email has already been registered"]
        except User.DoesNotExist:     
            pass  
        try:
            datetime.strptime(postData['DoB'], "%Y-%m-%d")
        except ValueError:
            results['status'] = False
            results['errors'] += ["This date is not in the accepted format (YYYY-MM-DD)"]
        return results

    def create_user(self, postData):
        password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = password, DoB = postData['DoB'])

    def login_validation(self, postData):
        results = {'errors':[], 'status':True}
        if len(self.filter(email=postData['email']))<1:
            results['status'] = False
            results['errors'] += ['This email has not been registered']
        else:
            password = self.get(email=postData['email']).password
            if not bcrypt.checkpw(postData['password'].encode(), password.encode()):
                results['status'] = False
                results['errors'] += ['This password is not the password we have recorded']
        return results

    def friend_validation(self, user1, user2):
        results = {'errors':[], 'status':True}
        if user1 == user2:
            results['status'] = False
            results['errors'] = ['You cannot be friends with yourself']
        for x in UserFriends.objects.filter(friend_of = user1):
            num2 = int(user2.id)
            if (x.friend_to_id == num2):
                results['status'] = False
                results['errors'] = ['They are already friends']
        return results

    def create_friends(self, user1, user2):
        UserFriends.objects.create(friend_of = user1, friend_to = user2)
        UserFriends.objects.create(friend_of = user2, friend_to = user1)

    def delete_friend(self, user1, user2):
        UserFriends.objects.get(friend_to = user1, friend_of = user2).delete()
        UserFriends.objects.get(friend_to = user2, friend_of = user1).delete()
    
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    DoB = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    friends = models.ManyToManyField("self", through = "UserFriends", related_name="friends_of", symmetrical=False)

class UserFriends(models.Model):
    friend_of = models.ForeignKey(User, related_name = "source")
    friend_to = models.ForeignKey(User, related_name = "target")
    objects = UserManager()