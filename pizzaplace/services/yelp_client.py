from pizzaplace.services.yelp_api_response_parser import YelpApiResponseParser
from meetup.services.http_client import HttpClient
from pizzaplace.services.yelp_url_builder import YelpUrlBuilder

class YelpClient():
  def __init__(self, yelp_url):
    self.http_client = HttpClient
    self.yelp_url_builder = YelpUrlBuilder(yelp_url)
    self.response_parser = YelpApiResponseParser
    self.request_components = self.yelp_url_builder.build_authorization_components()
    self.yelp_url = self.yelp_url_builder.build_api_url()

  def get_yelp_info(self):
    response = self.http_client.get_response(self.yelp_url, self.request_components)
    parsed_response = self.response_parser(response).parse()
    return parsed_response

  def exists(self):
    response = HttpClient.get_response(self.yelp_url, self.request_components)
    return response.status_code == 200
