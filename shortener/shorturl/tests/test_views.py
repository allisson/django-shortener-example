# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from shorturl.models import Link
from shorturl import dehydrate

class IndexViewTest(TestCase):

    def setUp(self):
        self.url = reverse('shorturl_index')
        self.user1 = User.objects.create_user(
            'user1',
            'user1@email.com',
            '123456'
        )
        self.register_url = reverse('accounts_register')
        self.login_url = reverse('accounts_login')
        self.logout_url = reverse('accounts_logout')
        self.my_links_url = reverse('shorturl_my_links')

    def test_render(self):
        # load view
        response = self.client.get(self.url)

        # check status code
        self.assertEquals(response.status_code, 200)
        
        # check links
        self.assertContains(response, self.register_url)
        self.assertContains(response, self.login_url)
        
    def test_render_with_logged_user(self):
        # login user
        self.client.login(username='user1', password='123456')
        
        # load view
        response = self.client.get(self.url)

        # check status code
        self.assertEquals(response.status_code, 200)
        
        # check links
        self.assertContains(response, self.logout_url)
        self.assertContains(response, self.my_links_url)


class AddLinkViewTest(TestCase):

    def setUp(self):
        self.url = reverse('shorturl_add_link')
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
            'url',
            u'Este campo é obrigatório.'
        )

    def test_valid_form(self):
        # load post
        response = self.client.post(
            self.url,
            {
                'url': u'http://allissonazevedo.com/',
            },
            follow=True
        )
        
        # check link
        link = Link.objects.get(id=1)
        self.assertEquals(link.url, u'http://allissonazevedo.com/')

        # check redirect
        self.assertRedirects(response, reverse('shorturl_show_link', args=[link.id]))

        # check message
        self.assertContains(
            response,
            u'Link encurtado com sucesso.'
        )
        
        
class ShowLinkViewTest(TestCase):

    def setUp(self):
        self.link = Link.objects.create_link('http://allissonazevedo.com/')
        self.url = reverse('shorturl_show_link', args=[self.link.id])

    def test_render(self):
        # load view
        response = self.client.get(self.url)

        # check status code
        self.assertEquals(response.status_code, 200)
        
        # check links
        self.assertContains(response, self.link.url)
        self.assertContains(response, self.link.get_short_url())


class RedirectLinkViewTest(TestCase):

    def setUp(self):
        self.link = Link.objects.create_link('http://allissonazevedo.com/')
        self.url = reverse('shorturl_redirect_link', args=[dehydrate(self.link.id)])

    def test_render(self):
        # load view
        response = self.client.get(self.url, follow=True)

        # check status code
        self.assertEquals(response.status_code, 200)
        
        # check redirect
        self.assertRedirects(response, self.link.url)


class MyLinksViewTest(TestCase):

    def setUp(self):
        self.url = reverse('shorturl_my_links')
        self.user1 = User.objects.create_user(
            'user1',
            'user1@email.com',
            '123456'
        )
        self.client.login(username='user1', password='123456')
        self.link1 = Link.objects.create_link('http://allissonazevedo.com/', user=self.user1)
        self.link2 = Link.objects.create_link('http://twitter.com/allisson', user=self.user1)

    def test_render_without_login(self):
        # logout user
        self.client.logout()

        # load view
        response = self.client.get(self.url)

        # check redirect
        self.assertRedirects(
            response, reverse('accounts_login') + '?next=' + self.url)

    def test_render(self):
        # load view
        response = self.client.get(self.url)

        # check status code
        self.assertEquals(response.status_code, 200)
        
        # check context
        self.assertTrue(self.link1 in response.context['links'])
        self.assertTrue(self.link2 in response.context['links'])
