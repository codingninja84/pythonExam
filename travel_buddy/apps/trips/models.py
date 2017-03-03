from __future__ import unicode_literals
from django.db import models
from ..users.models import User
from datetime import datetime


class TripManager(models.Manager):
    def createNew(self, formData, user_id):
        response = {}
        errors = []
        
        dateFrom = str(formData['travelfrom'])
        dateTo = str(formData['travelTo'])
        date_To_Object = datetime.strptime(dateTo, '%Y-%m-%d')
        date_From_Object = datetime.strptime(dateFrom, '%Y-%m-%d')
        if dateTo < dateFrom:
            errors.append("Start date must be before end date")
        if dateTo < str(datetime.now()) or dateFrom < str(datetime.now()):
            errors.append("Trip must be current or future date")
        if len(formData['destination']) < 3:
            errors.append("Must be a task longer than 3 char!")
        if len(formData['description']) < 3:
            errors.append("Must be a task longer than 3 char!")
        if errors:
            response['errors'] = errors
            response['status'] = False
            return response
        else:
            user = User.objects.get(id=user_id)
            trip = self.create(destination=formData['destination'], description=formData['description'], dateTo=formData['travelTo'], dateFrom=formData['travelfrom'], creator=user)
            trip.traveler.add(user)
            response['status'] = True
            return response

    def joinTrip(self, user_id, trip_id):
        user = User.objects.get(id=user_id)
        trip = Trip.objects.get(id=trip_id)
        trip.traveler.add(user)

class Trip(models.Model):
    destination = models.CharField(max_length=38)
    description = models.CharField(max_length= 38)
    dateTo = models.DateField(auto_now=False)
    dateFrom = models.DateField(auto_now=False)
    traveler = models.ManyToManyField(User, related_name= "User_trips")
    creator = models.ForeignKey(User, related_name="created_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
