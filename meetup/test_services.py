from django.test import TestCase
from meetup.services.endpoint import Endpoint
from meetuppizza.settings import base

class TestMeetupService(TestCase):
  pass

class TestEndpoint(TestCase):
  def test_returns_200_ok_from_valid_url(self):
    key = {"key": base.MEETUP_KEY }
    response = Endpoint.get_response('https://api.meetup.com/papers-we-love', key)
    self.assertEquals(200, response.status_code)

  def test_returns_404_for_invalid_url(self):
    key = {"key": base.MEETUP_KEY }
    response = Endpoint.get_response('https://api.meetup.com/made-up-meetup', key)
    self.assertEquals(404, response.status_code)
