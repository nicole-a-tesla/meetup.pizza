from meetup.services.meetup_api_response_parser import MeetupApiResponseParser
from meetup.services.http_client import HttpClient
from meetup.services.meetup_url_builder import MeetupUrlBuilder

class MeetupClient():
  def __init__(self, meetup_url):
    self.http_client = HttpClient
    self.meetup_url_builder = MeetupUrlBuilder(meetup_url)
    self.response_parser = MeetupApiResponseParser

  def get_meetup_info(self):
    request_components = self.meetup_url_builder.build_api_components()
    response = self.http_client.get_response(request_components)
    parsed_response = self.response_parser(response).parse()
    return parsed_response

