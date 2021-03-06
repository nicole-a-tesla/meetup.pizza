from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from model_utils.models import TimeStampedModel

from pizzaplace.services.yelp_client import YelpClient


def validate_url(url):
  validator = RegexValidator(
    regex='yelp.com/biz/\w+[-\w+]*(?:\?(?:.)*)?$',
    message="Url should be in form 'https://www.yelp.com/biz/some-pizza-place'",
    code='invalid_url')
  return validator(url)

def validate_yelp_business_exists(url):
  if not YelpClient(url).exists():
    raise ValidationError("Yelp Business not found on Yelp.com")

class PizzaPlace(TimeStampedModel):
  name = models.CharField(max_length=500, unique=True, default=None)
  yelp_url = models.URLField(max_length=500, unique=True, default=None, validators=[validate_url, validate_yelp_business_exists])

  def __str__(self):
    return self.name
