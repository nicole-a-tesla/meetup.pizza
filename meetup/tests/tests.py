from django.test import TestCase
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from unittest.mock import MagicMock
from unittest.mock import patch

from meetup.models import Meetup
from meetup.presenter.meetup_presenter import MeetupPresenter
from meetup.services.parsed_meetup_response import ParsedMeetupResponse
from meetup.services.meetup_api_response_parser import MeetupApiResponseParser
from pizzaplace.presenter.pizza_place_presenter import PizzaPlacePresenter



meetup_api_response = [{
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


class TestMeetupApiResponseParser(TestCase):
  def setUp(self):
    self.mock_response = HttpResponse()
    self.mock_response.json = MagicMock(return_value=meetup_api_response)
    self.meetup_api_response_parser = MeetupApiResponseParser(self.mock_response)

  def test_parsed_response_contains_venue(self):
    self.assertEquals(self.meetup_api_response_parser.parse().get('venue'), 'The Lexington')

  def test_parsed_response_contains_event_topic(self):
    self.assertEquals(self.meetup_api_response_parser.parse().get('next_event_topic'), 'Code & Coffee')

  def test_parsed_response_contains_event_datetime(self):
    self.assertEquals(self.meetup_api_response_parser.parse().get('datetime'), 1458730800000)

  def test_parsed_response_contains_lat_and_long(self):
    self.assertEquals(self.meetup_api_response_parser.parse().get('lat'), 40.75501251220703)
    self.assertEquals(self.meetup_api_response_parser.parse().get('lon'), -73.97337341308594)

  def test_handles_response_with_no_venue(self):
    venueless_response = [{
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
          }
        ]
    self.mock_response.json = MagicMock(return_value=venueless_response)
    # meetup_api_response_parser = MeetupApiResponseParser(venueless_response)
    self.assertEquals(self.meetup_api_response_parser.parse().get('venue'), 'No venue listed')
