from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from meetuppizza.forms import RegistrationForm
from meetup.models import Meetup
from meetup.services.meetup_info_fetch import MeetupInfoFetch
from meetup.services.meetup_api_lookup_agent import MeetupApiLookupAgent

def index(request):
  meetups = Meetup.objects.all()
  fat_meetups = MeetupInfoFetch(meetups, MeetupApiLookupAgent).fat_meetups()
  return render(request, 'index.html', {"meetups": fat_meetups})

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
