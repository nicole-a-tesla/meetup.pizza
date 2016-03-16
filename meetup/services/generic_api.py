from django.http import HttpResponse
import requests
from meetuppizza.settings import base

class GenericApi():
  BASE_URL = ''
  KEY = ''

  def __init__(self, link):
    self.link = link

  def get_response(self):
    api_url = self.build_api_url()
    url_components = {"key": self.KEY }

    return requests.get(api_url, params=url_components)

  def build_api_url(self):
    pass

  def url_exists(self):
    return self.get_response().status_code == 200


  def get_urlname(self):
    pass
