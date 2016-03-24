from django.test import TestCase
from django.test import RequestFactory

from unittest.mock import patch

from meetup.models import Meetup
from meetup.presenter.meetup_presenter import MeetupPresenter
from meetup.services.parsed_meetup_response import ParsedMeetupResponse
from meetuppizza.views import index

class TestLandingPage(TestCase):
  def setUp(self):
    self.raw_parsed_response = {'venue': 'The Lexington',
                            'next_event_topic': 'Code Coffee',
                            'datetime': 1458730800000,
                            'lat': '40.75501251220703',
                            'lon':  '-73.97337341308594'}
    self.parsed_meetup_response = ParsedMeetupResponse(self.raw_parsed_response)


    self.meetup = Meetup.objects.create(name='new meetup', meetup_url='http://www.meetup.com/papers-we-love/')
    self.meetup.pizza_places.create(name='Prince', yelp_url='https://www.yelp.com/biz/prince-st-pizza-new-york')
    self.patcher = patch('meetuppizza.views.MeetupService')
    self.mock_service = self.patcher.start()
    self.mock_service.return_value.get_decorated_meetup.return_value = MeetupPresenter(self.meetup, self.parsed_meetup_response)

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
