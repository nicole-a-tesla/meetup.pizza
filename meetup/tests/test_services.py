from django.test import TestCase
from django.conf import settings
from django.http import HttpResponse

from unittest.mock import patch

from meetup.services.http_client import HttpClient
from meetup.services.meetup_client import MeetupClient
from meetup.services.meetup_service import MeetupService
from meetup.services.parsed_meetup_response import ParsedMeetupResponse
from meetup.services import map_url_generator
from meetup.presenter.meetup_presenter import MeetupPresenter
from meetup.services.meetup_url_builder import MeetupUrlBuilder
from meetup.models import Meetup


valid_meetup_url = 'https://www.meetup.com/papers-we-love/'

class TestMeetupService(TestCase):
  def test_service_gets_info_from_meetup_client(self):
    meetup = Meetup(name="Ms. Meetup", meetup_url=valid_meetup_url)
    client_info = MeetupService(meetup).get_decorated_meetup()
    self.assertEquals('Ms. Meetup', client_info.meetup_name())

class TestMeetupClient(TestCase):

  @patch('meetup.services.meetup_client.MeetupApiResponseParser')
  def test_client_parsed_response_includes_venue(self, mock_response):
    parsed_response = {'venue': 'Someplace', 'next_event_topic': 'some topic', 'datetime': 1458730800000, 'lat': '40.689745', 'lon':  '-74.0476567'}
    mock_response.return_value.parse.return_value = parsed_response
    parsed_meetup_client_response = MeetupClient(valid_meetup_url).get_meetup_info()
    self.assertTrue('venue' in parsed_meetup_client_response)
    self.assertTrue('next_event_topic' in parsed_meetup_client_response)
    self.assertTrue('datetime' in parsed_meetup_client_response)
    self.assertTrue('lat' in parsed_meetup_client_response)
    self.assertTrue('lon' in parsed_meetup_client_response)

  @patch('meetup.services.http_client.requests')
  def test_meetup_url_exists(self, mock_http_requests):
    mock_http_requests.get.return_value = HttpResponse()
    meetup_client = MeetupClient('https://api.meetup.com/papers-we-love')
    self.assertTrue(meetup_client.exists())

class TestHttpClient(TestCase):
  def test_returns_200_ok_from_valid_url(self):
    key = {"key": settings.MEETUP_KEY }
    url = 'https://api.meetup.com/papers-we-love'
    args = {'params': key}
    response = HttpClient.get_response(url, args)
    self.assertEquals(200, response.status_code)

  def test_returns_404_for_invalid_url(self):
    key = {"key": settings.MEETUP_KEY }
    url = 'https://api.meetup.com/papers-we-HATE'
    args = {'params': key}
    response = HttpClient.get_response(url, args)
    self.assertEquals(404, response.status_code)

class TestUrlBuilder(TestCase):
  def test_build_api_url(self):
    api_url = MeetupUrlBuilder(valid_meetup_url).build_api_url()
    self.assertEquals('https://api.meetup.com/papers-we-love/events', api_url)

  @patch('meetup.services.meetup_url_builder.settings')
  def test_builds_authorization_hash(self, mock_settings):
    mock_settings.MEETUP_KEY = "FAKE KEY"
    components = MeetupUrlBuilder(valid_meetup_url).build_authorization_components()
    expected_params = {'key': "FAKE KEY"}
    self.assertEquals(expected_params, components['params'])

class TestParsedMeetupResponse(TestCase):
  def setUp(self):
    self.raw_parsed_response = {'venue'           : 'Someplace',
                                'next_event_topic': 'some topic',
                                'datetime'        : 1458730800000,
                                'lat'             : '40.689745',
                                'lon'             : '-74.0476567'}
    self.parsed_meetup_response = ParsedMeetupResponse(self.raw_parsed_response)

  def test_parsed_meetup_response_has_venue(self):
    self.assertEquals(self.raw_parsed_response['venue'], self.parsed_meetup_response.venue)

  def test_parsed_meetup_response_has_next_event_topic(self):
    self.assertEquals(self.raw_parsed_response['next_event_topic'], self.parsed_meetup_response.next_event_topic)

  def test_parsed_meetup_response_has_datetime(self):
    self.assertEquals(self.raw_parsed_response['datetime'], self.parsed_meetup_response.datetime)

  def test_parsed_meetup_response_has_lat(self):
    self.assertEquals(self.raw_parsed_response['lat'], self.parsed_meetup_response.lat)

  def test_parsed_meetup_response_has_lon(self):
    self.assertEquals(self.raw_parsed_response['lon'], self.parsed_meetup_response.lon)

class TestMapUrlGenerator(TestCase):
  def test_google_map_url_generator(self):
    self.assertEquals("https://www.google.com/maps?q=40.75501251220703,-73.97337341308594", map_url_generator.generate_google_url(40.75501251220703, -73.97337341308594))
