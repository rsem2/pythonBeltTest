# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from models import User, UserManager

def index(request):
    if 'userid' not in request.session:
        request.session['userid'] = None
    elif request.session['userid'] != None:
        string = '/profile/'+str(request.session['userid'])
        return redirect(string)
    return render(request, 'users_app/index.html')

def process(request):
    results = User.objects.register_validation(request.POST)
    if results['status'] == False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/')
    else: 
        User.objects.create_user(request.POST)
        request.session['userid'] = User.objects.last().id
        request.session['username'] = User.objects.last().name
        string = '/profile/'+str(request.session['userid'])
        return redirect(string)

def login_process(request):
    results = User.objects.login_validation(request.POST)
    if results['status'] == False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['userid'] = User.objects.get(email = request.POST['email']).id
        request.session['username'] = User.objects.get(email = request.POST['email']).name
        string = '/profile/'+str(request.session['userid'])
        return redirect(string)

def logout(request):
    request.session.flush()
    return redirect('/')
