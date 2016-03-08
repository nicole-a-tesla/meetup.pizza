from django.test import TestCase
from meetup.models import Meetup
from pizzaplace.models import PizzaPlace
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError
from meetup.services.meetup_api_lookup_agent import MeetupApiLookupAgent
from meetup.services.meetup_info_fetch import MeetupInfoFetch
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

  def test_string_representation_of_meetup(self):
    m = Meetup(name="Mr. Meetup", meetup_link='http://meetup.com/some-other-meetup')
    self.assertEquals("Mr. Meetup", str(m))

  def test_meetup_name_is_unique(self):
    m = Meetup(name="Meetup", meetup_link='http://meetup.com/some-meetup')
    m.save()
    n = Meetup(name="Meetup", meetup_link='http://meetup.com/some-other-meetup')
    self.assertRaises(IntegrityError, n.save)

  def test_meetup_link_is_unique(self):
    m = Meetup(name="Meetup", meetup_link='http://meetup.com/some-meetup')
    m.save()
    n = Meetup(name="Meetup new", meetup_link='http://meetup.com/some-meetup')
    self.assertRaises(IntegrityError, n.save)

  def test_getting_all_associated_pizzas(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://meetup.com/some-meetup')
    meetup.save()
    place = PizzaPlace(name="Pete Zazz")
    place.save()
    meetup.pizza_places.add(place)
    self.assertEquals(place, meetup.pizza_places.all()[0])

  def test_meetup_raises_error_on_invalid_url(self):
    meetup= Meetup(name="Meeetup1", meetup_link='hi/ok/what')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_link_does_not_point_to_meetupdotcom(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.example.com/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_no_urlname_in_meetup_url(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_no_trailing_slash_in_meetup_url(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/hackerhours')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_multiple_urlnames(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/hackerhours/events/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_meetup_url_with_urlname_and_trailing_slash_passes(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/hackerhours/')
    errors_raiesed_by_meetup = meetup.full_clean()
    self.assertTrue(errors_raiesed_by_meetup == None)

  def test_url_with_dashes_in_urlname_passes(self):
    meetup = Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/papers-we-love/')
    errors_raiesed_by_meetup = meetup.full_clean()
    self.assertIsNone(errors_raiesed_by_meetup)

  def test_non_real_meetup_raises_validation_error(self):
    meetup = Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/la-la-la/')
    self.assertRaises(ValidationError, meetup.full_clean)

class TestMeetupApi(TestCase):

  def test_can_parse_out_urlname(self):
    link = "https://meetup.com/Hello-Pizza/"
    lookup_agent = MeetupApiLookupAgent(link)
    urlname = lookup_agent.get_urlname()
    self.assertEquals("Hello-Pizza", urlname)

  def test_valid_url_returns_json_with_matching_name_attribute(self):
    link = "http://meetup.com/papers-we-love/"
    lookup_agent = MeetupApiLookupAgent(link)
    response = lookup_agent.get_response()
    meetup_name = response.json()['name']
    self.assertEqual(meetup_name, 'Papers We Love')

  def test_invalid_url_returns_404(self):
    link = "http://meetup.com/NONSENSE-NOTHING/"
    lookup_agent = MeetupApiLookupAgent(link)
    response = lookup_agent.get_response()
    self.assertEqual(response.status_code, 404)

  def test_validator_returns_true_for_valid_url(self):
    link = "http://meetup.com/papers-we-love/"
    lookup_agent = MeetupApiLookupAgent(link)
    is_valid = lookup_agent.is_real_meetup()
    self.assertTrue(is_valid)

  def test_validator_returns_false_for_invalid_url(self):
    link = "http://meetup.com/this-is-not-a-meetup/"
    lookup_agent = MeetupApiLookupAgent(link)
    is_valid = lookup_agent.is_real_meetup()
    self.assertFalse(is_valid)


  def test_events_lookup_returns_event(self):
    link = "http://meetup.com/papers-we-love/"
    lookup_agent = MeetupApiLookupAgent(link)
    response = lookup_agent.get_response('events')
    self.assertEqual(response.status_code, 200)


class TestMeetupInfoFetch(TestCase):

  def test_returns_meetup_collection(self):
    meetup = Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/papers-we-love/')
    i_fetch = MeetupInfoFetch([meetup])
    self.assertEqual(meetup.name, i_fetch.fat_meetups()[0].name)

  def test_fat_meetups_returns_at_least_one_event_venue_name(self):
    meetup = Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/Software-Craftsmanship-New-York/')
    i_fetch = MeetupInfoFetch([meetup])
    self.assertEquals('ThoughtWorks', i_fetch.fat_meetups()[0].venue)

  def test_fat_meetups_returns_at_least_one_next_event_topic(self):
    meetup = Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/Software-Craftsmanship-New-York/')
    i_fetch = MeetupInfoFetch([meetup])
    self.assertEquals('Hands-on session: Exploring Reactive Programming', i_fetch.fat_meetups()[0].next_event_topic)

  def test_fat_meetups_returns_at_least_one_next_event_time(self):
    meetup = Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/Software-Craftsmanship-New-York/')
    i_fetch = MeetupInfoFetch([meetup])
    self.assertEquals('Fri Sep 12 04:00:00', i_fetch.fat_meetups()[0].datetime)


