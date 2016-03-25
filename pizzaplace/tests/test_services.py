from django.test import TestCase
from django.conf import settings
from django.http import HttpResponse

from unittest.mock import MagicMock
from unittest.mock import patch

from meetup.services.http_client import HttpClient
from pizzaplace.models import PizzaPlace
from pizzaplace.services.yelp_url_builder import YelpUrlBuilder
from pizzaplace.services.yelp_client import YelpClient
from pizzaplace.services.yelp_service import YelpService
from pizzaplace.services.parsed_yelp_response import ParsedYelpResponse
from pizzaplace.services.yelp_api_response_parser import YelpApiResponseParser


valid_yelp_url = 'https://www.yelp.com/biz/prince-st-pizza-new-york'

class TestHttpClient(TestCase):
  def test_returns_200_ok_from_valid_url(self):
    auth = settings.YELP_OAUTH_OBJECT
    url = "https://api.yelp.com/v2/business/prince-st-pizza-new-york"
    args = {'auth': auth}
    response = HttpClient.get_response(url, args)
    self.assertEquals(200, response.status_code)

  def test_returns_404_for_invalid_url(self):
    auth = settings.YELP_OAUTH_OBJECT
    url = "https://api.yelp.com/v2/business/made-up-pizza-place"
    args = {'auth': auth}
    response = HttpClient.get_response(url, args)
    self.assertEquals(400, response.status_code)

class TestUrlBuilder(TestCase):
  def test_build_api_components(self):
    api_url = YelpUrlBuilder(valid_yelp_url).build_api_url()
    self.assertEquals("https://api.yelp.com/v2/business/prince-st-pizza-new-york", api_url)

  @patch('pizzaplace.services.yelp_url_builder.settings')
  def test_builds_authoriation_hash(self, mock_settings):
    mock_settings.YELP_OAUTH_OBJECT = "FAKE OAUTH"
    components = YelpUrlBuilder(valid_yelp_url).build_authorization_components()
    expected_params = "FAKE OAUTH"
    self.assertEquals(expected_params, components['auth'])

class TestParsedYelpResponse(TestCase):
  def setUp(self):
    self.raw_parsed_response = {'rating' : 5}
    self.parsed_yelp_response = ParsedYelpResponse(self.raw_parsed_response)

  def test_parsed_yelp_response_has_rating(self):
    self.assertEquals(self.raw_parsed_response['rating'], self.parsed_yelp_response.rating)

class TestYelpApiResponseParser(TestCase):
  def test_parsed_response_contains_rating(self):
    mock_response = HttpResponse()
    mock_response.json = MagicMock(return_value={'rating' : 4})
    yelp_api_response_parser = YelpApiResponseParser(mock_response)
    self.assertEquals(yelp_api_response_parser.parse().get('rating'), 4)

class TestYelpClient(TestCase):
  @patch('pizzaplace.services.yelp_client.YelpApiResponseParser')
  def test_client_parsed_includes_venue(self, mock_response):
    mock_response.return_value.parse.return_value = {'rating': 4}
    parsed_yelp_client_response = YelpClient(valid_yelp_url).get_yelp_info()
    self.assertTrue('rating' in parsed_yelp_client_response)

  @patch('pizzaplace.services.yelp_client.HttpClient')
  def test_yelp_url_exists(self, mock_http_response):
    mock_http_response.get_response.return_value = HttpResponse()
    yelp_client = YelpClient(valid_yelp_url)
    self.assertTrue(yelp_client.exists())

class TestYelpServices(TestCase):
  def test_service_gets_info_from_yelp_client(self):
    pizzaplace = PizzaPlace(name='Prince Street Pizza',yelp_url=valid_yelp_url)
    client_info = YelpService(pizzaplace).get_decorated_pizza_place()
    self.assertEquals('🍕🍕🍕🍕', client_info.pizza_place_rating())


