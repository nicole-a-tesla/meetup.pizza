from django.db import models
from django.http import HttpResponse
import requests
import os


class MeetupApiLookupAgent():
  def __init__(self, link):
    self.link = link

  def get_response(self):
    api_url = "https://api.meetup.com/" + self.get_urlname()
    url_components = {"key": os.getenv("MEETUP_KEY")}

    return requests.get(api_url, params=url_components)

  def is_real_meetup(self):
    return self.get_response().status_code == 200


  def get_urlname(self):
    return self.link.split('/')[-2]
