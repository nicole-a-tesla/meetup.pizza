from django.test import TestCase

from meetup.models import Meetup
from meetup.services.parsed_meetup_response import ParsedMeetupResponse
from pizzaplace.presenter.pizza_place_presenter import PizzaPlacePresenter
from meetup.presenter.meetup_presenter import MeetupPresenter


class TestMeetupPresenter(TestCase):

  def setUp(self):
    self.meetup = Meetup(name="Meetup1", meetup_url='http://www.meetup.com/papers-we-love/')
    self.raw_parsed_response = {'venue'           : 'The Lexington',
                                'next_event_topic': 'Code & Coffee',
                                'datetime'        : 1458730800000,
                                'lat'             : 40.75501251220703,
                                'lon'             : -73.97337341308594}
    self.parsed_meetup_response = ParsedMeetupResponse(self.raw_parsed_response)

    self.presenter = MeetupPresenter(self.meetup, self.parsed_meetup_response)

  def test_meetup_presenter_returns_meetup_url(self):
    self.assertEquals(self.presenter.meetup_url(), 'http://www.meetup.com/papers-we-love/')

  def test_meetup_presenter_returns_meetup_name(self):
    self.assertEquals(self.presenter.meetup_name(), 'Meetup1')

  def test_meetup_presenter_returns_meetup_venue(self):
    self.assertEquals('The Lexington', self.presenter.meetup_venue())

  def test_meetup_presenter_returns_meetup_next_topic(self):
    self.assertEquals('Code & Coffee', self.presenter.meetup_next_event_topic())

  def test_meetup_presenter_returns_meetup_datetime(self):
    self.assertEquals("03/23/2016, 07:00:00 AM EDT", self.presenter.meetup_datetime())

  def test_meetup_presenter_returns_meetup_map_url(self):
    self.assertEquals("https://www.google.com/maps?q=40.75501251220703,-73.97337341308594", self.presenter.meetup_map_url())

  def test_meetup_presenter_returns_pizza_place_presenters(self):
    self.meetup.save()
    pizza_place = self.meetup.pizza_places.create(name="Pizza place", yelp_url='https://www.yelp.com/biz/prince-st-pizza-new-york')
    self.assertIsInstance(self.presenter.meetup_pizza_places()[0], PizzaPlacePresenter)
