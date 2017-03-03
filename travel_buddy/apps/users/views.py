from django.shortcuts import render

from .models import User
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User
from datetime import datetime

def index(request):
    return render(request, ('users/index.html'))

def success(request):
    context = {
    'current': User.objects.get(id=request.session['id'])
    }
    return render(request, ('travels/travels.html'), context)
#
def register(request):
    if request.method == "POST":
        response = User.objects.register(request.POST)
        if response['status']:
            request.session['name'] = response['user'].user
            request.session['id'] = response['user'].id
            return redirect('travels:success')
        else:
            errors = response['errors']
            for error in errors:
                messages.error(request, error)
            return redirect('users:index')

def login(request):
    if request.method == "POST":
        response = User.objects.login(request.POST)
        if response['status']:
            request.session['name'] = response['user'].user
            request.session['id'] = response['user'].id
            return redirect('travels:success')
        else:
            errors = response['errors']
            for error in errors:
                messages.error(request, error)
            return redirect('users:index')
#
# def delete(request, apt_id):
#     Appointment.objects.deleteApt(apt_id)
#     return redirect('users:success')
def logout(request):
    request.session.clear()
    return redirect("users:index")
