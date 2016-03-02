from django.test import TestCase
from meetup.models import Meetup
from django.db import IntegrityError

class TestMeetup(TestCase):

  def test_meetup_is_a_thing(self):
    meetup = Meetup()
    self.assertIsInstance(meetup, Meetup)

  def test_create_meetup_with_name_and_id(self):
    meetup = Meetup(name='papers we love', meetup_id=1)
    self.assertEquals(meetup.name, 'papers we love')
    self.assertEquals(meetup.meetup_id, 1)

  def test_name_can_not_be_blank(self):
    meetup = Meetup(meetup_id=1)
    self.assertRaises(IntegrityError, meetup.save)

  def test_meetup_id_can_not_be_blank(self):
    meetup = Meetup(name='papers we love')
    self.assertRaises(IntegrityError, meetup.save)