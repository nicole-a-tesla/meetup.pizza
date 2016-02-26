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
  # email = request.POST.get('email')
  # password = request.POST.get('password')

  # new_user = User.objects.create_user(email, password)
  # user = authenticate(email=email, password=password)


  form = UserCreationForm(request.POST)

  if form.is_valid():
    form.save()
    return HttpResponseRedirect('/welcome')

  # if user is not None:
  #   login(request, user)
  #   return redirect('/welcome')
  else:
    return redirect('/')

def welcome(request):
  return render(request, 'welcome.html')