from django.conf import settings

import requests

from meetup.services.generic_api import GenericApi

class YelpApi(GenericApi):
  BASE_URL = "https://api.yelp.com/v2/business/"

  def get_response(self):
    url = self.build_api_url()
    auth = settings.YELP_OAUTH_OBJECT
    return requests.get(url, auth=auth)

  def build_api_url(self):
    return self.BASE_URL + self.get_unique_id()

  def get_unique_id(self):
    url_minus_queries = self.url.split('?')[0]
    return url_minus_queries.split('/')[-1]
