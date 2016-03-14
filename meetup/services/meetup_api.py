from django.db import models
from django.http import HttpResponse
import requests
import os
from meetuppizza.settings import base

class MeetupApi():
  def __init__(self, link):
    self.link = link

  def get_response(self, category=''):
    api_url = "https://api.meetup.com/" + self.get_urlname() + '/' + category
    url_components = {"key": base.MEETUP_KEY}

    return requests.get(api_url, params=url_components)

  def meetup_exists(self):
    return self.get_response().status_code == 200


  def get_urlname(self):
    return self.link.split('/')[-2]
