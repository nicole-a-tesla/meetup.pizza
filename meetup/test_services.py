from django.test import TestCase
from unittest.mock import patch
from meetup.services.http_client import HttpClient
from meetuppizza.settings import base
from meetup.services.meetup_client import MeetupClient

class TestMeetupService(TestCase):
  pass

class TestMeetupClient(TestCase):
  def test_build_api_components(self):
    api_url_components = MeetupClient().build_api_components('https://www.meetup.com/papers-we-love/')
    self.assertEquals('https://api.meetup.com/papers-we-love/events', api_url_components['url'])

  @patch('meetup.services.meetup_client.base')
  def test_builds_params_hash(self, mock_settings):
    mock_settings.MEETUP_KEY = "FAKE KEY"
    api_url_components = MeetupClient().build_api_components('https://www.meetup.com/papers-we-love/')
    expected_params = {'key': "FAKE KEY"}
    self.assertEquals(expected_params, api_url_components['params'])

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
