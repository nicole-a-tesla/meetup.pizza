from meetuppizza.settings import base
from meetup.services import meetup_api_response_parser
from meetup.services.http_client import HttpClient

class MeetupClient():
  def __init__(self, meetup_link):
    self.meetup_link = meetup_link
    self.http_client = HttpClient
    self.response_parser = meetup_api_response_parser

  def get_meetup_info(self):
    request_components = self.build_api_components()
    response = self.http_client.get_response(request_components)
    parsed_response = self.response_parser.parse(response)
    return parsed_response

  def build_api_components(self):
    url = self.build_api_url()
    params = self.build_params()
    return {'url': url, 'params': params}

  def get_unique_id(self):
    return self.meetup_link.split('/')[-2]

  def build_api_url(self):
    return "https://api.meetup.com/" + self.get_unique_id() + '/events'

  def build_params(self):
    return {"key": base.MEETUP_KEY }

