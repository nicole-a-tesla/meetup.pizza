from django.test import TestCase
from meetup.models import Meetup
from pizzaplace.models import PizzaPlace
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError
from meetup.services.meetup_api import MeetupApi
from meetup.services.meetup_presenter import MeetupPresenter
from meetup.services import meetup_api_response_parser
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch
from django.http import HttpResponse


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

  def test_valid_meetup_has_name_and_link(self):
    meetup = Meetup(name='papers we love', meetup_link='http://meetup.com/some-meetup')
    self.assertEquals(meetup.name, 'papers we love')
    self.assertEquals(meetup.meetup_link, 'http://meetup.com/some-meetup')

  def test_blank_meetup_link_raises_integrity_error(self):
    meetup = Meetup(meetup_link='http://meetup.com/some-meetup')
    self.assertRaises(IntegrityError, meetup.save)

  def test_blank_meetup_name_raises_integrity_error(self):
    meetup = Meetup(name='papers we love')
    self.assertRaises(IntegrityError, meetup.save)

  def test_meetup_name_can_not_be_over_500_characters(self):
    name = 'x' *501
    meetup = Meetup(name=name, meetup_link='http://meetup.com/some-meetup')
    self.assertRaises(DataError, meetup.save)

  def test_string_representation_of_meetup_is_its_name(self):
    m = Meetup(name="Mr. Meetup", meetup_link='http://meetup.com/some-other-meetup')
    self.assertEquals("Mr. Meetup", str(m))

  def test_meetup_name_is_unique(self):
    m = Meetup.objects.create(name="Meetup", meetup_link='http://meetup.com/some-meetup')
    n = Meetup(name="Meetup", meetup_link='http://meetup.com/some-other-meetup')
    self.assertRaises(IntegrityError, n.save)

  def test_meetup_link_is_unique(self):
    m = Meetup.objects.create(name="Meetup", meetup_link='http://meetup.com/some-meetup')
    n = Meetup(name="Meetup new", meetup_link='http://meetup.com/some-meetup')
    self.assertRaises(IntegrityError, n.save)

  def test_getting_all_associated_pizzas(self):
    meetup= Meetup.objects.create(name="Meetup1", meetup_link='http://meetup.com/some-meetup')
    place = meetup.pizza_places.create(name="Pete Zazz")
    self.assertEquals(place, meetup.pizza_places.first())

class TestMeetupModelValidations(TestCase):

  def setUp(self):
    self.patcher = patch('meetup.models.MeetupApi')
    self.mock_agent = self.patcher.start()

  def test_meetup_raises_error_on_invalid_url(self):
    meetup= Meetup(name="Meetup1", meetup_link='hi/ok/what')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_link_does_not_point_to_meetupdotcom(self):
    meetup= Meetup(name="Meetup1", meetup_link='http://www.example.com/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_no_urlname_in_meetup_url(self):
    meetup= Meetup(name="Meetup1", meetup_link='http://www.meetup.com/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_no_trailing_slash_in_meetup_url(self):
    meetup= Meetup(name="Meetup1", meetup_link='http://www.meetup.com/hackerhours')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_multiple_urlnames(self):
    meetup= Meetup(name="Meetup1", meetup_link='http://www.meetup.com/hackerhours/events/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_meetup_url_with_urlname_and_trailing_slash_passes(self):
    meetup= Meetup(name="Meetup1", meetup_link='http://www.meetup.com/hackerhours/')
    errors_raiesed_by_meetup = meetup.full_clean()
    self.assertTrue(errors_raiesed_by_meetup == None)

  def test_url_with_dashes_in_urlname_passes(self):
    meetup = Meetup(name="Meetup1", meetup_link='http://www.meetup.com/papers-we-love/')
    errors_raiesed_by_meetup = meetup.full_clean()
    self.assertIsNone(errors_raiesed_by_meetup)

  def test_non_real_meetup_raises_validation_error(self):
    self.mock_agent.return_value.url_exists.return_value = False
    meetup = Meetup(name="Meetup1", meetup_link='http://www.meetup.com/la-la-la/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def tearDown(self):
    self.addCleanup(self.patcher.stop)


class TestMeetupApi(TestCase):

  def test_can_parse_out_urlname(self):
    lookup_agent = self.lookup_agent_builder("https://meetup.com/Hello-Pizza/")
    urlname = lookup_agent.get_urlname()
    self.assertEquals("Hello-Pizza", urlname)

  def test_invalid_url_returns_404(self):
    lookup_agent = self.lookup_agent_builder("http://meetup.com/NONSENSE-NOTHING/")
    response = lookup_agent.get_response()
    self.assertEqual(response.status_code, 404)

  def test_validator_returns_true_for_valid_url(self):
    lookup_agent = self.lookup_agent_builder("http://meetup.com/papers-we-love/")
    is_valid = lookup_agent.url_exists()
    self.assertTrue(is_valid)

  def test_validator_returns_false_for_invalid_url(self):
    lookup_agent = self.lookup_agent_builder("http://meetup.com/this-is-not-a-meetup/")
    is_valid = lookup_agent.url_exists()
    self.assertFalse(is_valid)

  def test_events_lookup_returns_event(self):
    lookup_agent = self.lookup_agent_builder("http://meetup.com/papers-we-love/")
    response = lookup_agent.get_response()
    self.assertEqual(response.status_code, 200)

  def lookup_agent_builder(self, link):
    return MeetupApi(link)


class TestMeetupPresenter(TestCase):

  def setUp(self):
    self.info = {'venue'            : 'Some place',
                 'next_event_topic' : 'awesome stuff',
                 'datetime'         : 1426723243000,
                 'lat'              : 40.75501251220703,
                 'lon'              : -73.97337341308594}
    self.meetup = Meetup(name="Meetup1", meetup_link='http://www.meetup.com/papers-we-love/')

  def test_meetup_presenter_returns_meetup_link(self):
    presenter = MeetupPresenter(self.meetup, self.info)
    self.assertEquals(presenter.get_meetup_link(), 'http://www.meetup.com/papers-we-love/')

  def test_meetup_presenter_returns_meetup_name(self):
    presenter = MeetupPresenter(self.meetup, self.info)
    self.assertEquals(presenter.get_meetup_name(), 'Meetup1')

  def test_meetup_presenter_returns_meetup_venue(self):
    presenter = MeetupPresenter(self.meetup, self.info)
    self.assertEquals(presenter.get_meetup_venue(), 'Some place')

  def test_meetup_presenter_returns_meetup_next_topic(self):
    presenter = MeetupPresenter(self.meetup, self.info)
    self.assertEquals(presenter.get_meetup_next_event_topic(), 'awesome stuff')

  def test_meetup_presenter_returns_meetup_datetime(self):
    presenter = MeetupPresenter(self.meetup, self.info)
    self.assertEquals(presenter.get_meetup_datetime(), "Thu Jan 22 11:56:40")

  def test_meetup_presenter_returns_meetup_map_link(self):
    presenter = MeetupPresenter(self.meetup, self.info)
    self.assertEquals(presenter.get_meetup_map_link(), "https://www.google.com/maps?q=40.75501251220703,-73.97337341308594")

  @patch("meetup.services.meetup_api.MeetupApi")
  def test_meetup_presenter_returns_pizza_places(self, fake_api):
    self.meetup.save()
    pizza_place = self.meetup.pizza_places.create(name="Pizza place")
    presenter = MeetupPresenter(self.meetup, self.info)
    self.assertEquals(presenter.get_meetup_pizza_places().first(), pizza_place)


class TestMeetupApiResponseParser(TestCase):
  def setUp(self):
    self.mockResponse = HttpResponse()
    self.mockResponse.json = MagicMock(return_value=meetup_api_response)

  def test_parsed_response_contains_venue(self):
    self.assertEquals(meetup_api_response_parser.parse(self.mockResponse).get('venue'), 'The Lexington')

  def test_parsed_response_contains_event_topic(self):
    self.assertEquals(meetup_api_response_parser.parse(self.mockResponse).get('next_event_topic'), 'Code & Coffee')

  def test_parsed_response_contains_event_datetime(self):
    self.assertEquals(meetup_api_response_parser.parse(self.mockResponse).get('datetime'), 1458730800000)

  def test_parsed_response_contains_lat_and_long(self):
    self.assertEquals(meetup_api_response_parser.parse(self.mockResponse).get('lat'), 40.7599983215332)
    self.assertEquals(meetup_api_response_parser.parse(self.mockResponse).get('lon'), -73.98999786376953)
