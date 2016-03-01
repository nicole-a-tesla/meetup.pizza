from django.db import models

# Create your models here.
class Meetup(models.Model):
  name = models.CharField(max_length=500)