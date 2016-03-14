from django.db import models
from pizzaplace.models import PizzaPlace
from django.core.validators import RegexValidator
from meetup.services.meetup_api_lookup_agent import MeetupApiLookupAgent
from django.core.exceptions import ValidationError
from model_utils.models import TimeStampedModel

def validate_urlname(link):
  validator = RegexValidator(
    regex='meetup\.com\/\w+(-\w+)*\/$',
    message="Url should be in form 'meetup.com/meetup-name/'",
    code='invalid_url')
  return validator(link)

def validate_meetup_exists(link):
  if not MeetupApiLookupAgent(link).meetup_exists():
    raise ValidationError("Meetup not found on meetup.com")
    

class Meetup(TimeStampedModel):
  name = models.CharField(max_length=500, null=False, blank=False, default=None, unique=True)
  meetup_link = models.URLField(max_length=500,
                                unique=True,
                                default=None,
                                validators=[validate_urlname, validate_meetup_exists])
  pizza_places = models.ManyToManyField(PizzaPlace)

  def __str__(self):
    return self.name


