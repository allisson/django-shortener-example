# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings


class RegisterViewTest(TestCase):

    def setUp(self):
        self.url = reverse('accounts_register')
        self.user1 = User.objects.create_user(
            'user1',
            'user1@email.com',
            '123456'
        )

    def test_render(self):
        # load view
        response = self.client.get(self.url)

        # check status code
        self.assertEquals(response.status_code, 200)

    def test_empty_form(self):
        # load post
        response = self.client.post(self.url)

        # check form errors
        self.assertFormError(
            response,
            'form',
            'name',
            u'Este campo é obrigatório.'
        )
        self.assertFormError(
            response,
            'form',
            'username',
            u'Este campo é obrigatório.'
        )
        self.assertFormError(
            response,
            'form',
            'email',
            u'Este campo é obrigatório.'
        )
        self.assertFormError(
            response,
            'form',
            'password1',
            u'Este campo é obrigatório.'
        )
        self.assertFormError(
            response,
            'form',
            'password2',
            u'Este campo é obrigatório.'
        )

    def test_form_with_dont_match_passwords(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'password1': '123456',
                'password2': '1234567',
                }
        )

        # check form errors
        self.assertFormError(
            response,
            'form',
            'password2',
            u'As duas senhas não conferem.'
        )

    def test_form_with_registered_username(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'username': 'user1',
            }, follow=True
        )

        # check form errors
        self.assertFormError(
            response,
            'form',
            'username',
            u'Nome de usuário já cadastrado.'
        )

    def test_form_with_upper_username(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'username': 'User1',
            }, follow=True
        )

        # check form errors
        self.assertFormError(
            response,
            'form',
            'username',
            u'Use apenas caracteres minúsculos para o nome de usuário.'
        )

    def test_form_with_invalid_username(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'username': 'user1@email.com',
            }, follow=True
        )

        # check form errors
        self.assertFormError(
            response,
            'form',
            'username',
            u'Use apenas letras e números para o nome de usuário.'
        )
        
    def test_form_with_registered_email(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'email': 'user1@email.com',
            }, follow=True
        )

        # check form errors
        self.assertFormError(
            response,
            'form',
            'email',
            u'E-mail já cadastrado.'
        )

    def test_valid_form(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'name': u'User Two',
                'username': u'user2',
                'email': u'user2@email.com',
                'password1': u'123456',
                'password2': u'123456'
            },
            follow=True
        )

        # check redirect
        self.assertRedirects(response, reverse('shorturl_index'))

        # check message
        self.assertContains(
            response,
            u'Conta criada com sucesso.'
        )

        # check user
        self.assertTrue(User.objects.filter(username=u'user2'))


class LoginViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'user1',
            'user1@email.com',
            '123456'
        )
        self.url = reverse('accounts_login')

    def test_render(self):
        # load view
        response = self.client.get(self.url)

        # check status code
        self.assertEquals(response.status_code, 200)

    def test_empty_form(self):
        # load post
        response = self.client.post(self.url)

        # check form errors
        self.assertFormError(
            response,
            'form',
            'username',
            u'Este campo é obrigatório.'
        )
        self.assertFormError(
            response,
            'form',
            'password',
            u'Este campo é obrigatório.'
        )

    def test_form_with_invalid_username(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'username': 'user2',
            }
        )

        # check form errors
        self.assertFormError(
            response,
            'form',
            'username',
            u'Nome de usuário não cadastrado.'
        )

    def test_form_with_invalid_password(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'username': 'user1',
                'password': '1234567',
            }
        )

        # check form errors
        self.assertFormError(
            response,
            'form',
            'password',
            u'Senha inválida.'
        )

    def test_form_with_inactive_account(self):
        # make account inactive
        self.user1.is_active = False
        self.user1.save()

        # load post
        response = self.client.post(
            self.url,
            {
                'username': 'user1',
                'password': '123456',
            }, follow=True
        )

        # check form errors
        self.assertFormError(
            response,
            'form',
            None,
            u'Conta inativa.'
        )

    def test_valid_form(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'username': 'user1',
                'password': '123456',
            }, follow=True
        )
        # check redirect
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

    def test_form_valid_with_next(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'username': 'user1',
                'password': '123456',
                'next': '/entrar/',
            }, follow=True
        )

        # check redirect
        self.assertRedirects(response, reverse('accounts_login'))
