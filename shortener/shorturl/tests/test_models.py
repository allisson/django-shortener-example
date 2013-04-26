# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from shorturl.models import Link


class LinkModelTest(TestCase):

    def test_manager_create_link(self):
        # generate new link
        link = Link.objects.create_link('http://allissonazevedo.com')
        
        # check link
        self.assertEquals(link.id, 1)
        self.assertEquals(link.url, 'http://allissonazevedo.com')
        self.assertEquals(link.hash_url, '166f9c9ba72ac00903f8ea3c3e1c6578')
        
        # generate new link again
        link = Link.objects.create_link('http://allissonazevedo.com')
        
        # check link
        self.assertEquals(link.id, 1)
        self.assertEquals(link.url, 'http://allissonazevedo.com')
        self.assertEquals(link.hash_url, '166f9c9ba72ac00903f8ea3c3e1c6578')
        
    def test_manager_create_link_with_user(self):
        # create users
        user1 = User.objects.create_user(
            'user1',
            'user1@email.com',
            '123456'
        )
        user2 = User.objects.create_user(
            'user2',
            'user2@email.com',
            '123456'
        )
        
        # generate new link
        link = Link.objects.create_link('http://allissonazevedo.com', user=user1)
        
        # check link
        self.assertEquals(link.id, 1)
        self.assertEquals(link.url, 'http://allissonazevedo.com')
        self.assertEquals(link.hash_url, '166f9c9ba72ac00903f8ea3c3e1c6578')
        self.assertTrue(user1 in link.users.all())
        
        # generate new link with another user
        link = Link.objects.create_link('http://allissonazevedo.com', user=user2)
        
        # check link
        self.assertEquals(link.id, 1)
        self.assertEquals(link.url, 'http://allissonazevedo.com')
        self.assertEquals(link.hash_url, '166f9c9ba72ac00903f8ea3c3e1c6578')
        self.assertTrue(user2 in link.users.all())
