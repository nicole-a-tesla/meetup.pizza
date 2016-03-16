from django.http import HttpResponse
import requests
from meetuppizza.settings import base
from meetup.services.generic_api import GenericApi

class MeetupApi(GenericApi):
  CATEGORY = 'events'
  BASE_URL = "https://api.meetup.com/"
  KEY = base.MEETUP_KEY

  def __init__(self, link):
    self.link = link

  def build_api_url(self):
    return self.BASE_URL + self.get_urlname() + '/' + self.CATEGORY

  def get_urlname(self):
    return self.link.split('/')[-2]
