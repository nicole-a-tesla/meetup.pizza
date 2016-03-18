from django.http import HttpResponse
import requests
from meetuppizza.settings import base

class GenericApi():
  BASE_URL = ''

  def __init__(self, link):
    self.link = link

  def get_response(self):
    pass

  def build_api_url(self):
    pass

  def url_exists(self):
    return self.get_response().status_code == 200

  def get_unique_id(self):
    pass
