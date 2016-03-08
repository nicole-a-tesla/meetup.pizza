from django.db import models

# Create your models here.
class PizzaPlace(models.Model):
  name = models.CharField(max_length=500, unique=True, default=None)

  def __str__(self):
    return self.name 