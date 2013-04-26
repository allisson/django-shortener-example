# -*- coding: utf-8 -*-
from django import forms

from shorturl.models import Link

class LinkForm(forms.Form):

    url = forms.URLField(
        label=u'URL',
        max_length=250,
        required=True,
        help_text=u'Insira o endereço que você deseja encurtar.'
    )
    
    def __init__(self, *args, **kwargs):
        # load super class
        super(LinkForm, self).__init__(*args, **kwargs)
        
        # add field size
        self.fields['url'].widget.attrs['class'] = 'text'

    def save(self, user=None):
        # get url
        url = self.cleaned_data.get('url')

        # create new link
        link = Link.objects.create_link(url, user=user)

        # return link
        return link
