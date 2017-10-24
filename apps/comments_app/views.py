# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from ..users_app.models import User, UserFriends

# Create your views here.
def profile(request, num):

    ## Make sure only people logged in can see this page
    if request.session['userid'] == None:
        return redirect('/')

    user = User.objects.get(id=request.session['userid'])
    
    ## make a list of friends and everyone else
    friends = user.friends.all()
    notfriends = User.objects.all()

    for friend in friends:
        notfriends = notfriends.exclude(id = friend.id)

    notfriends = notfriends.exclude(id = request.session['userid'])
    context = {
        'friends': friends,
        'notfriends': notfriends,
    }
    return render(request, 'profile.html', context)

def add_friend(request, num1, num2):
    ## find both people in the friendship
    user1 = User.objects.get(id=num1)
    user2 = User.objects.get(id=num2)

    ## make sure they aren't trying to be friends with themselves or someoen they are already friends with
    results = User.objects.friend_validation(user1,user2)
    if results['status'] == False:
        for error in results['errors']:
            messages.error(request, error)
    else: 
        User.objects.create_friends(user1,user2)

    ## redirect back to their profile
    string = '/profile/'+str(num1)
    return redirect(string)

def remove(request, num):
    user1 = User.objects.get(id=request.session['userid'])
    user2 = User.objects.get(id=num)
    UserFriends.objects.delete_friend(user1, user2)
    string = '/profile/'+str(request.session['userid'])
    return redirect(string)

def other_profile(request, num):
    ## Make sure only people logged in can see this page
    if request.session['userid'] == None:
        return redirect('/')
    context = {
        'user': User.objects.get(id=num)
    }
    return render(request, 'other_profile.html', context)