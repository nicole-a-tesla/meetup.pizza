from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
import pdb

def index(request):
  return render(request, 'index.html')

def sign_up(request):
  if request.method == 'GET':
    args = {}
    args['form'] = UserCreationForm()
    return render(request, 'sign_up.html', args)

  if request.method == 'POST':
    form = UserCreationForm(request.POST)

    if form.is_valid():
      form.save()

      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(request, user)

      return redirect('/welcome')
    else:
      return render(request, 'sign_up.html', {'form': form})

def welcome(request):
  return render(request, 'welcome.html')
