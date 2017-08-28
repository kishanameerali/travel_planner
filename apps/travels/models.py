from __future__ import unicode_literals
from django.db import models
from ..users.models import User

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = []
        if len(postData['destination']) < 1 or len(postData['description']) < 1:
            errors.append('Fields Can Not Be Blank')
        if len(postData['travel_date_from']) < 1 or len(postData['travel_date_to']) < 1:
            errors.append('Please Enter All Dates')
        if postData['travel_date_from'] > postData['travel_date_to']:
            errors.append('From Date Must Be Before To Date')
        return errors

    def create_trip(self, clean_data, id):
        Trip.objects.create(
            destination = clean_data['destination'],
            description = clean_data['description'],
            travel_date_from = clean_data['travel_date_from'],
            travel_date_to = clean_data['travel_date_to'],
            planner = User.objects.get(id=id)
        )


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    planner = models.ForeignKey(User, related_name='planned_trips')
    joiners = models.ManyToManyField(User, related_name='joined_trips')
    objects = TripManager()

    def __str__(self):
        return '{}, from: {}, return: {}, planner: {}'.format(self.destination, self.travel_date_from, self.travel_date_to, self.planner)