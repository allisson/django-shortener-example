# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterForm(forms.Form):

    name = forms.CharField(
        label=u'Nome',
        min_length=3,
        required=True,
        help_text=u'Seu nome completo.'
    )

    username = forms.RegexField(
        label=u'Nome de usuário',
        regex=r'^[\w]+$',
        error_messages={
            'invalid': u'Use apenas letras e números para o nome de usuário.'
        },
        min_length=3,
        max_length=30,
        required=True,
        help_text=u'Escolha um nome de usuário (login).'
    )
    
    email = forms.EmailField(
        label=u'E-mail',
        required=True,
        help_text=u'Informe seu e-mail para criação da conta.'
    )

    password1 = forms.CharField(
        label=u'Senha',
        max_length=16,
        min_length=6,
        required=True,
        widget=forms.PasswordInput,
        help_text=u'Escolha uma senha com seis caracteres ou mais.'
    )
    password2 = forms.CharField(
        label=u'Confirmar senha',
        max_length=16,
        min_length=6,
        required=True,
        widget=forms.PasswordInput,
        help_text=u'Repita a senha escolhida acima.'
    )
    
    def __init__(self, *args, **kwargs):
        # load super class
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        # add field size
        self.fields['name'].widget.attrs['class'] = 'text'
        self.fields['username'].widget.attrs['class'] = 'text'
        self.fields['email'].widget.attrs['class'] = 'text'
        self.fields['password1'].widget.attrs['class'] = 'text'
        self.fields['password2'].widget.attrs['class'] = 'text'

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        if User.objects.filter(username=username):
            raise forms.ValidationError(u'Nome de usuário já cadastrado.')
        if username != username.lower():
            raise forms.ValidationError(u'Use apenas caracteres minúsculos para o nome de usuário.')
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if User.objects.filter(email=email):
            raise forms.ValidationError(u'E-mail já cadastrado.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', None)
        password2 = self.cleaned_data.get('password2', None)
        if password1 != password2:
            raise forms.ValidationError(u'As duas senhas não conferem.')
        return password2

    def save(self):
        # get fields
        password = self.cleaned_data.get('password2')
        name = self.cleaned_data.get('name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        # create user
        user = User.objects.create_user(username, email, password)
        split_name = name.split(' ', 1)
        user.first_name = split_name[0]
        if len(split_name) == 2:
            user.last_name = split_name[1]
        user.save()

        # return user authenticated
        return authenticate(username=username, password=password)


class LoginForm(forms.Form):
    
    username = forms.CharField(
        label=u'Nome de usuário',
        required=True,
        help_text=u'Entre com seu nome de usuário (login).'
    )
    password = forms.CharField(
        label=u'Senha',
        required=True,
        widget=forms.PasswordInput,
        help_text=u'Entre com sua senha.'
    )

    def __init__(self, *args, **kwargs):
        # load super class 
        super(LoginForm, self).__init__(*args, **kwargs)
        
        # add field size
        self.fields['username'].widget.attrs['class'] = 'text'
        self.fields['password'].widget.attrs['class'] = 'text'

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        if not User.objects.filter(username=username):
            raise forms.ValidationError(u'Nome de usuário não cadastrado.')
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username', None)
        password = self.cleaned_data.get('password', None)
        if not authenticate(username=username, password=password):
            raise forms.ValidationError(u'Senha inválida.')
        return password

    def clean(self):
        username = self.cleaned_data.get('username', None)
        password = self.cleaned_data.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                raise forms.ValidationError(u'Conta inativa.')
        return self.cleaned_data

    def save(self):
        username = self.cleaned_data.get('username', None)
        password = self.cleaned_data.get('password', None)
        return authenticate(username=username, password=password)
