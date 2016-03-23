
import requests

from meetup.services.generic_api import GenericApi
from meetuppizza.settings import base

class MeetupApi(GenericApi):
  CATEGORY = 'events'
  BASE_URL = "https://api.meetup.com/"
  KEY = base.MEETUP_KEY

  def get_response(self):
    api_url = self.build_api_url()
    url_components = {"key": self.KEY }

    return requests.get(api_url, params=url_components)

  def build_api_url(self):
    return self.BASE_URL + self.get_unique_id() + '/' + self.CATEGORY

  def get_unique_id(self):
    return self.url.split('/')[-2]
