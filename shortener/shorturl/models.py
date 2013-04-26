# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

import hashlib
from shorturl import dehydrate


class LinkManager(models.Manager):
    
    def create_link(self, url, user=None):
        # generate hash url
        hash_url = hashlib.md5(url).hexdigest()
        
        # check if link exists
        try:
            link = self.model.objects.get(hash_url=hash_url)
        except self.model.DoesNotExist:
            link = self.model.objects.create(url=url, hash_url=hash_url)
        
        # if user, add to users
        if user:
            link.users.add(user)
        
        # return link
        return link
        

class Link(models.Model):
    
    url = models.URLField(
        u'URL',
        max_length=250
    )
    
    hash_url = models.CharField(
        u'Hash da URL',
        max_length=32,
        db_index=True
    )
    
    users = models.ManyToManyField(
        User,
        verbose_name=u'Usuários',
        related_name='my_links'
    )
    
    objects = LinkManager()
    
    # Audit fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = u'Link'
        verbose_name_plural = u'Links'
        
    def get_short_url(self):
        site = Site.objects.get_current()
        return 'http://%s/%s' % (site.domain, dehydrate(self.id))
