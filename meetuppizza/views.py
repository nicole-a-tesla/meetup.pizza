from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from meetuppizza.forms import RegistrationForm
from meetup.models import Meetup
from meetup.services.meetup_service import MeetupService

def index(request):
  meetups = Meetup.objects.all()
  meetup_presenters = []
  for meetup in meetups:
    service = MeetupService(meetup)
    meetup_presenters.append(service.get_decorated_meetup())
  return render(request, 'index.html', {"meetups": meetup_presenters})
