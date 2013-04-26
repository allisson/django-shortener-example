# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shorturl.forms import LinkForm
from shorturl.models import Link
from shorturl import saturate

def index(request):
    return render(request, 'shorturl/index.html')
    

def add_link(request):
    # get user
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    
    # process form
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(user=user)
            messages.success(request, u'Link encurtado com sucesso.')
            return redirect('shorturl_show_link', id=link.id)
    else:
        form = LinkForm()
    return render(request, 'shorturl/add_link.html', {'form': form})


def show_link(request, id):
    link = get_object_or_404(Link, id=id)
    return render(request, 'shorturl/show_link.html', {'link': link})


def redirect_link(request, base_62):
    id = saturate(base_62)
    link = get_object_or_404(Link, id=id)
    return redirect(link.url)


@login_required
def my_links(request):
    links = Link.objects.filter(users=request.user)
    return render(request, 'shorturl/my_links.html', {'links': links})
