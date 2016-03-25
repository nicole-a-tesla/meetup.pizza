from django.conf import settings

class YelpUrlBuilder():
  BASE_URL = "https://api.yelp.com/v2/business/"

  def __init__(self, yelp_url):
    self.yelp_url = yelp_url

  def build_api_url(self):
    return self.BASE_URL + self.get_unique_id()

  def build_authorization_components(self):
    return { 'auth': settings.YELP_OAUTH_OBJECT }

  def get_unique_id(self):
    url_minus_queries = self.yelp_url.split('?')[0]
    return url_minus_queries.split('/')[-1]
