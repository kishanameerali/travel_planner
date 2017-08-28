from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'users/index.html')

def register(request):
    validations = User.objects.validator(request.POST)
    if len(validations) == 0:
        new_user = User.objects.create_user(request.POST)
        request.session['id'] = new_user.id
        messages.success(request, "Hello {}!".format(new_user.username))
        return redirect('/travels')
    else:
        for errors in validations:
            messages.error(request, errors)
        return redirect('/')

def login(request):
    login_result = User.objects.login_validator(request.POST)
    if login_result[0]:
        for error in login_result[0]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['id'] = login_result[1].id
        messages.success(request, "Hello {}!".format(login_result[1].username))
        return redirect('/travels')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')