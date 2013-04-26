# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.conf import settings

from accounts.forms import RegisterForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # get new user
            new_user = form.save()

            # login new user
            auth_login(request, new_user)

            # make message
            messages.success(request, u'Conta criada com sucesso.')

            # redirect to index
            return redirect('shorturl_index')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login(request):
    # get next parameter
    next = request.REQUEST.get('next', settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(next)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'next': next})
