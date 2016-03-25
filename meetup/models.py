from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from model_utils.models import TimeStampedModel

from meetup.services.meetup_client import MeetupClient
from pizzaplace.models import PizzaPlace

def validate_urlname(url):
  validator = RegexValidator(
    regex='meetup.com/\w+[-\w+]*/$',
    message="Url should be in form 'http://meetup.com/meetup-name'",
    code='invalid_url')
  return validator(url)

def validate_meetup_exists(url):
  if not MeetupClient(url).exists():
    raise ValidationError("Meetup not found on meetup.com")


class Meetup(TimeStampedModel):
  name = models.CharField(max_length=500, default=None, unique=True)
  meetup_url = models.URLField(max_length=500,
                                unique=True,
                                default=None,
                                validators=[validate_urlname, validate_meetup_exists])
  pizza_places = models.ManyToManyField(PizzaPlace)

  def __str__(self):
    return self.name


