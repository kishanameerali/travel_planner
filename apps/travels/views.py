from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import Trip
from ..users.models import User
from django.contrib import messages

def travel_index(request):
    logged_user = User.objects.get(id=request.session['id'])
    scheduled_trips = logged_user.planned_trips.all()
    scheduled_trips_joined = logged_user.joined_trips.all()
    other_trips = Trip.objects.all().exclude(planner=logged_user).exclude(joiners=logged_user)
    return render(request, 'travels/travel_index.html', {'trips': scheduled_trips, 'joined_trips': scheduled_trips_joined, 'other_trips': other_trips, })

def destination(request, id):
    the_destination = Trip.objects.get(id=id)
    return render(request, 'travels/travel_destination.html', {'place': the_destination})

def add(request):
    return render(request, 'travels/travel_add.html')

def add_trip(request):
    validations = Trip.objects.trip_validator(request.POST)
    if validations:
        for error in validations:
            messages.error(request, error)
    else:
        Trip.objects.create_trip(request.POST, request.session['id'])
    return redirect('/travels')

def join_trip(request, id):
    req_trip = Trip.objects.get(id=id)
    req_trip.joiners.add(User.objects.get(id=request.session['id']))
    return redirect('/travels')




