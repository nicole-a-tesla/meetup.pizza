from django.test import TestCase
from unittest.mock import patch
from meetup.services.http_client import HttpClient
from meetuppizza.settings import base
from meetup.services.meetup_client import MeetupClient
from meetup.services.meetup_service import MeetupService
from meetup.services.meetup_presenter import MeetupPresenter
from meetup.services.meetup_url_builder import MeetupUrlBuilder
from meetup.models import Meetup


valid_meetup_url = 'https://www.meetup.com/papers-we-love/'

class TestMeetupService(TestCase):
  def test_service_gets_info_from_meetup_client(self):
    meetup = Meetup(name="Ms. Meetup", meetup_link=valid_meetup_url)
    client_info = MeetupService(meetup).get_decorated_meetup()
    self.assertIsInstance(client_info, MeetupPresenter)

class TestMeetupClient(TestCase):

  @patch('meetup.services.meetup_client.meetup_api_response_parser')
  def test_client_parsed_response_includes_venue(self, mock_response):
    parsed_response = {'venue': 'Someplace', 'next_event_topic': 'some topic', 'datetime': 1458730800000, 'lat': '40.689745', 'lon':  '-74.0476567'}
    mock_response.parse.return_value = parsed_response
    parsed_meetup_client_response = MeetupClient(valid_meetup_url).get_meetup_info()
    self.assertTrue('venue' in parsed_meetup_client_response)
    self.assertTrue('next_event_topic' in parsed_meetup_client_response)
    self.assertTrue('datetime' in parsed_meetup_client_response)
    self.assertTrue('lat' in parsed_meetup_client_response)
    self.assertTrue('lon' in parsed_meetup_client_response)

class TestHttpClient(TestCase):
  def test_returns_200_ok_from_valid_url(self):
    key = {"key": base.MEETUP_KEY }
    args = {'url': 'https://api.meetup.com/papers-we-love',
             'params': key}
    response = HttpClient.get_response(args)
    self.assertEquals(200, response.status_code)

  def test_returns_404_for_invalid_url(self):
    key = {"key": base.MEETUP_KEY }
    args = {'url': 'https://api.meetup.com/papers-we-HATE',
             'params': key}
    response = HttpClient.get_response(args)
    self.assertEquals(404, response.status_code)

class TestUrlBuilder(TestCase):
  def test_build_api_components(self):
    api_url_components = MeetupUrlBuilder(valid_meetup_url).build_api_components()
    self.assertEquals('https://api.meetup.com/papers-we-love/events', api_url_components['url'])

  @patch('meetup.services.meetup_url_builder.base')
  def test_builds_params_hash(self, mock_settings):
    mock_settings.MEETUP_KEY = "FAKE KEY"
    api_url_components = MeetupUrlBuilder(valid_meetup_url).build_api_components()
    expected_params = {'key': "FAKE KEY"}
    self.assertEquals(expected_params, api_url_components['params'])

