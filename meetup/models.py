from django.db import models

# Create your models here.
class Meetup(models.Model):
  name = models.CharField(max_length=500, null=False, blank=False, default=None, unique=True)
  meetup_id = models.PositiveIntegerField(unique=True)

  def __str__(self):
    return self.name
