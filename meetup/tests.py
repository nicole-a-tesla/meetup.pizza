from django.test import TestCase
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from unittest.mock import MagicMock
from unittest.mock import patch

from meetup.models import Meetup
from meetup.services.meetup_api import MeetupApi
from meetup.services.meetup_presenter import MeetupPresenter
from meetup.services.meetup_api_response_parser import MeetupApiResponseParser
from pizzaplace.services.pizza_place_presenter import PizzaPlacePresenter



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


class TestMeetup(TestCase):

  def test_meetup_is_a_thing(self):
    meetup = Meetup()
    self.assertIsInstance(meetup, Meetup)

  def test_valid_meetup_has_name_and_url(self):
    meetup = Meetup(name='papers we love', meetup_url='http://meetup.com/some-meetup')
    self.assertEquals(meetup.name, 'papers we love')
    self.assertEquals(meetup.meetup_url, 'http://meetup.com/some-meetup')

  def test_blank_meetup_url_raises_integrity_error(self):
    meetup = Meetup(meetup_url='http://meetup.com/some-meetup')
    self.assertRaises(IntegrityError, meetup.save)

  def test_blank_meetup_name_raises_integrity_error(self):
    meetup = Meetup(name='papers we love')
    self.assertRaises(IntegrityError, meetup.save)

  def test_meetup_name_can_not_be_over_500_characters(self):
    name = 'x' *501
    meetup = Meetup(name=name, meetup_url='http://meetup.com/some-meetup')
    self.assertRaises(DataError, meetup.save)

  def test_string_representation_of_meetup_is_its_name(self):
    m = Meetup(name="Mr. Meetup", meetup_url='http://meetup.com/some-other-meetup')
    self.assertEquals("Mr. Meetup", str(m))

  def test_meetup_name_is_unique(self):
    m = Meetup.objects.create(name="Meetup", meetup_url='http://meetup.com/some-meetup')
    n = Meetup(name="Meetup", meetup_url='http://meetup.com/some-other-meetup')
    self.assertRaises(IntegrityError, n.save)

  def test_meetup_url_is_unique(self):
    m = Meetup.objects.create(name="Meetup", meetup_url='http://meetup.com/some-meetup')
    n = Meetup(name="Meetup new", meetup_url='http://meetup.com/some-meetup')
    self.assertRaises(IntegrityError, n.save)

  def test_getting_all_associated_pizzas(self):
    meetup= Meetup.objects.create(name="Meetup1", meetup_url='http://meetup.com/some-meetup')
    place = meetup.pizza_places.create(name="Pete Zazz", yelp_url='https://www.yelp.com/biz/prince-st-pizza-new-york')
    self.assertEquals(place, meetup.pizza_places.first())

class TestMeetupModelValidations(TestCase):

  def setUp(self):
    self.patcher = patch('meetup.models.MeetupApi')
    self.mock_agent = self.patcher.start()

  def test_meetup_raises_error_on_invalid_url(self):
    meetup= Meetup(name="Meetup1", meetup_url='hi/ok/what')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_url_does_not_point_to_meetupdotcom(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.example.com/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_no_urlname_in_meetup_url(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.meetup.com/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_no_trailing_slash_in_meetup_url(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.meetup.com/hackerhours')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_multiple_urlnames(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.meetup.com/hackerhours/events/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_meetup_url_with_urlname_and_trailing_slash_passes(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.meetup.com/hackerhours/')
    errors_raiesed_by_meetup = meetup.full_clean()
    self.assertTrue(errors_raiesed_by_meetup == None)

  def test_url_with_dashes_in_urlname_passes(self):
    meetup = Meetup(name="Meetup1", meetup_url='http://www.meetup.com/papers-we-love/')
    errors_raiesed_by_meetup = meetup.full_clean()
    self.assertIsNone(errors_raiesed_by_meetup)

  def test_non_real_meetup_raises_validation_error(self):
    self.mock_agent.return_value.exists.return_value = False
    meetup = Meetup(name="Meetup1", meetup_url='http://www.meetup.com/la-la-la/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def tearDown(self):
    self.addCleanup(self.patcher.stop)


class TestMeetupApi(TestCase):

  def test_can_parse_out_urlname(self):
    lookup_agent = self.lookup_agent_builder("https://meetup.com/Hello-Pizza/")
    urlname = lookup_agent.get_unique_id()
    self.assertEquals("Hello-Pizza", urlname)

  def test_invalid_url_returns_404(self):
    lookup_agent = self.lookup_agent_builder("http://meetup.com/NONSENSE-NOTHING/")
    response = lookup_agent.get_response()
    self.assertEqual(response.status_code, 404)

  def test_validator_returns_true_for_valid_url(self):
    lookup_agent = self.lookup_agent_builder("http://meetup.com/papers-we-love/")
    is_valid = lookup_agent.exists()
    self.assertTrue(is_valid)

  def test_validator_returns_false_for_invalid_url(self):
    lookup_agent = self.lookup_agent_builder("http://meetup.com/this-is-not-a-meetup/")
    is_valid = lookup_agent.exists()
    self.assertFalse(is_valid)

  def lookup_agent_builder(self, url):
    return MeetupApi(url)


class TestMeetupPresenter(TestCase):

  def setUp(self):
    self.meetup = Meetup(name="Meetup1", meetup_url='http://www.meetup.com/papers-we-love/')
    parsed_response = {'venue': 'The Lexington', 'next_event_topic': 'Code & Coffee', 'datetime': 1458730800000, 'lat': 40.75501251220703, 'lon':  -73.97337341308594}
    self.presenter = MeetupPresenter(self.meetup, parsed_response)

  def test_meetup_presenter_returns_meetup_url(self):
    self.assertEquals(self.presenter.get_meetup_url(), 'http://www.meetup.com/papers-we-love/')

  def test_meetup_presenter_returns_meetup_name(self):
    self.assertEquals(self.presenter.get_meetup_name(), 'Meetup1')

  def test_meetup_presenter_returns_meetup_venue(self):
    self.assertEquals('The Lexington', self.presenter.get_meetup_venue())

  def test_meetup_presenter_returns_meetup_next_topic(self):
    self.assertEquals('Code & Coffee', self.presenter.get_meetup_next_event_topic())

  def test_meetup_presenter_returns_meetup_datetime(self):
    self.assertEquals("03/23/2016, 07:00:00 AM EDT", self.presenter.get_meetup_datetime())

  def test_meetup_presenter_returns_meetup_map_url(self):
    self.assertEquals("https://www.google.com/maps?q=40.75501251220703,-73.97337341308594", self.presenter.get_meetup_map_url())

  def test_meetup_presenter_returns_pizza_place_presenters(self):
    self.meetup.save()
    pizza_place = self.meetup.pizza_places.create(name="Pizza place", yelp_url='https://www.yelp.com/biz/prince-st-pizza-new-york')
    self.assertIsInstance(self.presenter.get_meetup_pizza_places()[0], PizzaPlacePresenter)


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
