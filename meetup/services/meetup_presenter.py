import time
import datetime

from django.utils.timezone import make_aware

from pytz import timezone

from pizzaplace.services.pizza_place_presenter import PizzaPlacePresenter
from pizzaplace.services.yelp_api import YelpApi

class MeetupPresenter():
  def __init__(self, meetup, parsed_response):
    self.meetup = meetup
    self.parsed_api_response = parsed_response

  def get_meetup_link(self):
    return self.meetup.meetup_link

  def get_meetup_name(self):
    return self.meetup.name

  def get_meetup_venue(self):
    return self.parsed_api_response.get('venue')

  def get_meetup_next_event_topic(self):
    return self.parsed_api_response.get('next_event_topic')

  def get_meetup_datetime(self):
    time_string = self.parsed_api_response.get('datetime')
    utc_time = datetime.datetime.fromtimestamp(int(time_string) / 1000)
    eastern_time = make_aware(utc_time).strftime('%m/%d/%Y, %I:%M:%S %p %Z')
    return eastern_time

  def get_meetup_map_link(self):
    lat = self.parsed_api_response.get('lat')
    lon = self.parsed_api_response.get('lon')
    return "https://www.google.com/maps?q=%s,%s" % (lat, lon)

  def get_meetup_pizza_places(self):
    pizza_place_presenters = []
    for pizza_place in self.meetup.pizza_places.all():
      pizza_place_presenters.append(PizzaPlacePresenter(pizza_place, YelpApi))
    return pizza_place_presenters



