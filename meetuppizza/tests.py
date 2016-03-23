from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.test import RequestFactory

from unittest import mock
from unittest.mock import patch

from meetup.models import Meetup
from meetup.services.meetup_api import MeetupApi
from meetup.services import meetup_api_response_parser
from meetup.services.meetup_presenter import MeetupPresenter
from meetuppizza.forms import RegistrationForm
from meetuppizza.views import index
from pizzaplace.models import PizzaPlace


params = {
      'username':'Bjorn',
      'email':'bjorn@bjorn.com',
      'password1':'bjornbjorn',
      'password2':'bjornbjorn'
    }

class TestLandingPage(TestCase):
  def setUp(self):
    parsed_response = {'venue': 'The Lexington', 'next_event_topic': 'Code Coffee', 'datetime': 1458730800000, 'lat': '40.75501251220703', 'lon':  '-73.97337341308594'}
    self.meetup = Meetup.objects.create(name='new meetup', meetup_url='http://www.meetup.com/papers-we-love/')
    self.meetup.pizza_places.create(name='Prince', yelp_url='https://www.yelp.com/biz/prince-st-pizza-new-york')
    self.patcher = patch('meetuppizza.views.MeetupService')
    self.mock_service = self.patcher.start()
    self.mock_service.return_value.get_decorated_meetup.return_value = MeetupPresenter(self.meetup, parsed_response)

    self.request = RequestFactory().get("/")


  def test_landing_page_contains_pizza(self):
    response = index(self.request)
    self.assertContains(response, "pizza")

  def test_meetup_is_displayed_on_landing_page(self):
    response = index(self.request)
    self.assertContains(response, "The Lexington")

  def test_meetups_pizza_places_are_displayed_on_landing_page(self):
    response = index(self.request)
    self.assertContains(response, 'Prince')

  def test_multiple_meetup_pizza_places_are_displayed_on_landing_page(self):
    self.meetup.pizza_places.create(name='PizzOOO', yelp_url='https://www.yelp.com/biz/lombardis-pizza-new-york')
    response = index(self.request)
    self.assertContains(response, 'Prince')
    self.assertContains(response, 'PizzOOO')

  def test_meetups_pizza_places_ratings_are_displayed_on_landing_page(self):
    response = index(self.request)
    self.assertContains(response, '🍕🍕🍕🍕')

  def test_next_meetup_location_displayed(self):
    response = index(self.request)
    self.assertContains(response, "The Lexington")

  def test_next_meetup_time_displayed(self):
    response = index(self.request)
    self.assertContains(response, "03/23/2016, 07:00:00 AM EDT")

  def test_next_meetup_title_displayed(self):
    response = index(self.request)
    self.assertContains(response, "Code Coffee")

  def test_landing_page_contains_yelp_url(self):
    response = index(self.request)
    self.assertContains(response, "https://www.yelp.com/biz/prince-st-pizza-new-york")

  def test_landing_page_contains_map_url(self):
    response = index(self.request)
    self.assertContains(response, "https://www.google.com/maps?q=40.75501251220703,-73.97337341308594")

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
