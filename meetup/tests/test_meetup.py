from django.test import TestCase
from django.db import IntegrityError, DataError

from meetup.models import Meetup


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
    name = 'x' * 501
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
    meetup = Meetup.objects.create(name="Meetup1", meetup_url='http://meetup.com/some-meetup')
    place = meetup.pizza_places.create(name="Pete Zazz", yelp_url='https://www.yelp.com/biz/prince-st-pizza-new-york')
    self.assertEquals(place, meetup.pizza_places.first())
