from django.test import TestCase, Client
from django.contrib.auth.models import User
from meetuppizza.forms import RegistrationForm
from meetup.models import Meetup
from pizzaplace.models import PizzaPlace
from meetup.services.meetup_api import MeetupApi
from django.contrib import auth
from django.shortcuts import render, redirect
from django.test import RequestFactory
from unittest import mock
from unittest.mock import patch
from meetuppizza.views import index
from django.test import RequestFactory
from meetup.services import meetup_api_response_parser


params = {
      'username':'Bjorn',
      'email':'bjorn@bjorn.com',
      'password1':'bjornbjorn',
      'password2':'bjornbjorn'
    }

class TestLandingPage(TestCase):
  def setUp(self):
    self.meetup_info = [
        {
          "created": 1426723243000,
          "duration": 5400000,
          "group": {
            "created": 1391476627000,
            "name": "Software Craftsmanship New York",
            "id": 12705402,
            "join_mode": "approval",
            "lat": 40.7599983215332,
            "lon": -73.98999786376953,
            "urlname": "Software-Craftsmanship-New-York",
            "who": "craftsmen"
          },
          "id": "ldxfglyvfbfc",
          "link": "http://www.meetup.com/Software-Craftsmanship-New-York/events/229387692/",
          "name": "Code & Coffee",
          "status": "upcoming",
          "time": 1458730800000,
          "updated": 1453163859000,
          "utc_offset": -14400000,
          "yes_rsvp_count": 1,
          "waitlist_count": 0,
          "description": "<p>Do you like getting up early and starting the day with inspiring conversations or even better",
            "venue": {
              "id": 23708903,
              "name": "The Lexington",
              "lat": 40.75501251220703,
              "lon": -73.97337341308594,
              "address_1": "511 Lexington Ave",
              "city": "New York",
              "country": "us",
              "localized_country_name": "USA",
              "zip": "",
              "state": "NY"
            },
          }
        ]
    self.patcher = patch('meetuppizza.views.MeetupApi')
    self.mock_agent = self.patcher.start()
    self.mock_agent.return_value.get_response.return_value.json.return_value = self.meetup_info
    self.meetup = Meetup.objects.create(name='new meetup', meetup_link='http://www.meetup.com/papers-we-love/')
    self.request = RequestFactory().get("/")


  def test_landing_page_contains_pizza(self):
    response = index(self.request)
    self.assertContains(response, "pizza")

  def test_meetup_is_displayed_on_landing_page(self):
    response = index(self.request)
    self.assertContains(response, "The Lexington")

  def test_meetups_pizza_places_are_displayed_on_landing_page(self):
    self.meetup.pizza_places.create(name='Pizza!?', yelp_link='https://www.yelp.com/biz/prince-st-pizza-new-york')
    response = index(self.request)
    self.assertContains(response, 'Pizza!?')

  def test_multiple_meetup_pizza_places_are_displayed_on_landing_page(self):
    self.meetup.pizza_places.create(name='Pizza!?', yelp_link='https://www.yelp.com/biz/prince-st-pizza-new-york')
    self.meetup.pizza_places.create(name='PizzOOO', yelp_link='https://www.yelp.com/biz/lombardis-pizza-new-york')
    response = index(self.request)
    self.assertContains(response, 'Pizza!?')
    self.assertContains(response, 'PizzOOO')

  def test_meetups_pizza_places_ratings_are_displayed_on_landing_page(self):
    self.meetup.pizza_places.create(name='Prince', yelp_link='https://www.yelp.com/biz/prince-st-pizza-new-york')
    response = index(self.request)
    self.assertContains(response, '🍕🍕🍕🍕')

  def test_next_meetup_location_displayed(self):
    response = index(self.request)
    self.assertContains(response, "The Lexington")

  def test_next_meetup_time_displayed(self):
    response = index(self.request)
    self.assertContains(response, "Mon May  4 08:00:00")

  def test_next_meetup_title_displayed(self):
    response = index(self.request)
    self.assertContains(response, "Code &amp; Coffee")

  def test_landing_page_contains_map_link(self):
    response = index(self.request)
    self.assertContains(response, "https://www.google.com/maps?q=40.7599983215332,-73.98999786376953")

  def tearDown(self):
    self.addCleanup(self.patcher.stop)


class TestUserAuthentication(TestCase):

  def test_user_is_created_on_signup(self):
    self.client.post('/sign_up', params)
    user = User.objects.get(username='Bjorn')
    self.assertIsNotNone(user)

  def test_user_is_logged_in_after_signup(self):
    self.client.post('/sign_up', params)
    user = User.objects.get(username='Bjorn')
    self.assertFalse(user.is_anonymous())

  def test_user_is_anonyoous_after_log_out(self):
    self.client.post('/sign_up', params)
    self.client.get('/sign_out')
    user = auth.get_user(self.client)
    self.assertTrue(user.is_anonymous())

  def test_user_is_not_anonymous_after_login(self):
    self.client.post('/sign_up', params)
    self.client.get('/sign_out')
    login_params = {
      'username':'Bjorn',
      'password':'bjornbjorn',
    }
    self.client.post('/sign_in', login_params)
    user = auth.get_user(self.client)
    self.assertFalse(user.is_anonymous())

  def test_user_is_anonymous_if_login_is_invalid(self):
    login_params = {
      'username':'Birds',
      'password':'argulonic',
    }
    self.client.post('/sign_in', login_params)
    user = auth.get_user(self.client)
    self.assertTrue(user.is_anonymous())

  def test_raises_error_if_email_not_provided_on_signup(self):
    params = {
      'username':'Bjorn',
      'email':'',
      'password1':'bjornbjorn',
      'password2':'bjornbjorn'
    }
    self.client.post('/sign_up', params)
    user = auth.get_user(self.client)
    self.assertTrue(user.is_anonymous())
