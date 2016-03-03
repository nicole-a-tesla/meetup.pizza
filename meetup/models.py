from django.db import models
from pizzaplace.models import PizzaPlace

class Meetup(models.Model):
  name = models.CharField(max_length=500, null=False, blank=False, default=None, unique=True)
  meetup_link = models.CharField(max_length=500,unique=True, default=None)
  pizza_places = models.ManyToManyField(PizzaPlace)

  def __str__(self):
    return self.name
