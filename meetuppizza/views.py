from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from meetuppizza.forms import RegistrationForm
from meetup.models import Meetup
from meetup.services.meetup_api import MeetupApi
from meetup.services.meetup_presenter import MeetupPresenter
from meetup.services import meetup_api_response_parser
from meetup.services.meetup_service import MeetupService

def index(request):
  meetups = Meetup.objects.all()
  meetup_presenters = []
  for meetup in meetups:
    service = MeetupService(meetup)
    meetup_presenters.append(service.get_decorated_meetup())
  return render(request, 'index.html', {"meetups": meetup_presenters})

def sign_up(request):
  if request.method == 'GET':
    context = {}
    context['form'] = RegistrationForm().as_ul
    return render(request, 'sign_up.html', context)

  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()

      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)

        return redirect('/')
    else:
      return render(request, 'sign_up.html', {'form': form})


def sign_out(request):
  logout(request)
  return redirect('/')

def sign_in(request):
  if request.method == 'GET':
    return render(request, 'sign_in.html')

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else:
      error = "The username or password were incorrect."
      return render(request, 'sign_in.html',  {'error': error})
