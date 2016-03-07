from django.test import TestCase
from meetup.models import Meetup
from pizzaplace.models import PizzaPlace
from django.db import IntegrityError, DataError
from django.core.exceptions import ValidationError

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
    meetup= Meetup(name="Meeetup1", meetup_link='hi')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_link_does_not_point_to_meetupdotcom(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.example.com/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_no_urlname_in_meetup_url(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_no_trailing_slash_in_meetup_url(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/lalala')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_multiple_urlnames(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/lalala/whatever/')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_meetup_url_with_urlname_and_trailing_slash_passes(self):
    meetup= Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/lalala/')
    errors_raiesed_by_meetup = meetup.full_clean()
    self.assertTrue(errors_raiesed_by_meetup == None)

  def test_url_with_dashes_in_urlname_passes(self):
    meetup = Meetup(name="Meeetup1", meetup_link='http://www.meetup.com/la-la-la/')
    errors_raiesed_by_meetup = meetup.full_clean()
    self.assertIsNone(errors_raiesed_by_meetup)

