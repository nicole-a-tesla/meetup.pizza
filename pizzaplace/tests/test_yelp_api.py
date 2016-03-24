from django.test import TestCase

from pizzaplace.services.yelp_api import YelpApi

class TestYelpApi(TestCase):

  def test_can_parse_out_business_id(self):
    lookup_agent = YelpApi('https://www.yelp.com/biz/prince-st-pizza-new-york')
    business_id = lookup_agent.get_unique_id()
    self.assertEquals('prince-st-pizza-new-york', business_id)

  def test_can_parse_out_business_id_from_search_url(self):
    lookup_agent = YelpApi('https://www.yelp.com/biz/prince-st-pizza-new-york?osq=prince+street+pizza')
    business_id = lookup_agent.get_unique_id()
    self.assertEquals('prince-st-pizza-new-york', business_id)

  def test_invalid_url_returns_400(self):
    lookup_agent = YelpApi('https://www.yelp.com/biz/not-a-real-place')
    response = lookup_agent.get_response()
    self.assertEquals(400, response.status_code)

  def test_validator_returns_true_for_valid_url(self):
    lookup_agent = YelpApi("https://www.yelp.com/biz/prince-st-pizza-new-york")
    is_valid = lookup_agent.exists()
    self.assertTrue(is_valid)

  def test_validator_returns_false_for_invalid_url(self):
    lookup_agent = YelpApi("https://www.yelp.com/biz/this-is-not-a-meetup")
    is_valid = lookup_agent.exists()
    self.assertFalse(is_valid)
