from django.test import TestCase
from django.core.exceptions import ValidationError

from unittest.mock import patch

from meetup.models import Meetup

class TestMeetupModelValidations(TestCase):

  def setUp(self):
    self.patcher = patch('meetup.models.MeetupClient')
    self.mock_agent = self.patcher.start()
    self.invalid_url_format_message = "Url should be in form 'http://meetup.com/meetup-name'"

  def test_meetup_raises_error_on_invalid_url(self):
    meetup= Meetup(name="Meetup1", meetup_url='hi/ok/what')
    self.assertRaises(ValidationError, meetup.full_clean)

  def test_error_raised_if_url_does_not_point_to_meetupdotcom(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.example.com/')
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      meetup.full_clean()

  def test_error_raised_if_no_urlname_in_meetup_url(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.meetup.com/')
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      meetup.full_clean()

  def test_error_raised_if_no_trailing_slash_in_meetup_url(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.meetup.com/hackerhours')
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      meetup.full_clean()

  def test_error_raised_if_multiple_urlnames(self):
    meetup= Meetup(name="Meetup1", meetup_url='http://www.meetup.com/hackerhours/events/')
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      meetup.full_clean()

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
    with self.assertRaisesRegexp(ValidationError, 'Meetup not found on meetup.com'):
      meetup.full_clean()

  def tearDown(self):
    self.addCleanup(self.patcher.stop)
