from django.db import models
from model_utils.models import TimeStampedModel

class PizzaPlace(TimeStampedModel):
  name = models.CharField(max_length=500, unique=True, default=None)

  def __str__(self):
    return self.name
