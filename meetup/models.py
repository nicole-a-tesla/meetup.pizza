from django.db import models
from pizzaplace.models import PizzaPlace
from django.core.validators import RegexValidator
from meetup.services.meetup_api_lookup_agent import MeetupApiLookupAgent
from django.core.exceptions import ValidationError


def validate_urlname(link):
  validator = RegexValidator(
    regex='meetup\.com\/\w+(-\w+)*\/$',
    message="Does not conform to Meetup Url",
    code='invalid_url')
  return validator(link)

def validate_meetup_exists(link):
  looker = MeetupApiLookupAgent(link)
  is_real = looker.is_real_meetup()

  if not is_real:
    raise ValidationError("That's not a meetup")




class Meetup(models.Model):
  name = models.CharField(max_length=500, null=False, blank=False, default=None, unique=True)
  meetup_link = models.URLField(max_length=500,
                                unique=True,
                                default=None,
                                validators=[validate_urlname, validate_meetup_exists])
  pizza_places = models.ManyToManyField(PizzaPlace)
  venue = ''
  next_event_topic = ''
  datetime = ''
  map_link = ''

  def __str__(self):
    return self.name


