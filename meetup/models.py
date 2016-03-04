from django.db import models
from pizzaplace.models import PizzaPlace
from django.core.validators import RegexValidator
import pdb

def validate_urlname(link):
  validator = RegexValidator(
    regex='meetup\.com\/\w+(-\w+)*\/$',
    message="Does not conform to Meetup Url",
    code='invalid_url')
  return validator(link)



class Meetup(models.Model):
  name = models.CharField(max_length=500, null=False, blank=False, default=None, unique=True)
  meetup_link = models.URLField(max_length=500,
                                unique=True,
                                default=None, 
                                validators=[validate_urlname])
  pizza_places = models.ManyToManyField(PizzaPlace)

  def __str__(self):
    return self.name


