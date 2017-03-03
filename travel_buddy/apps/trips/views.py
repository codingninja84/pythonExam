from django.shortcuts import render, redirect
from ..users.models import User
from django.contrib import messages
from .models import Trip
from ..users.models import User

def success(request):
    current = User.objects.get(id=request.session['id'])
    context = {
    'current': current,
    'myTrips' : Trip.objects.filter(traveler=current),
    'otherTrips': Trip.objects.exclude(traveler=current)
    }
    return render(request, ('trips/trips.html'), context)

def create_plan(request):
    return render(request, ('trips/new.html'))

def new_trip(request):
    user_id = request.session['id']
    response = Trip.objects.createNew(request.POST, user_id)
    if response['status']:
        return redirect("travels:success")
    else:
        errors = response['errors']
        for error in errors:
            messages.error(request, error)
        return redirect("travels:create_plan")

def view(request, trip_id):
    context = {
    "trip" : Trip.objects.get(id=trip_id)
    }
    return render(request, ('trips/destination.html'), context)

def join(request, trip_id):
    user_id = request.session['id']
    Trip.objects.joinTrip(user_id, trip_id)
    return redirect("travels:success")
