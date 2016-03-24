import datetime

from django.utils.timezone import make_aware

from pizzaplace.presenter.pizza_place_presenter import PizzaPlacePresenter
from pizzaplace.services.yelp_api import YelpApi

class MeetupPresenter():
  def __init__(self, meetup, parsed_response):
    self.meetup = meetup
    self.parsed_api_response = parsed_response

  def meetup_url(self):
    return self.meetup.meetup_url

  def meetup_name(self):
    return self.meetup.name

  def meetup_venue(self):
    return self.parsed_api_response.venue

  def meetup_next_event_topic(self):
    return self.parsed_api_response.next_event_topic

  def meetup_datetime(self):
    time_string = self.parsed_api_response.datetime
    utc_time = datetime.datetime.fromtimestamp(int(time_string) / 1000)
    eastern_time = make_aware(utc_time).strftime('%m/%d/%Y, %I:%M:%S %p %Z')
    return eastern_time

  def meetup_map_url(self):
    lat = self.parsed_api_response.lat
    lon = self.parsed_api_response.lon
    return "https://www.google.com/maps?q=%s,%s" % (lat, lon)

  def meetup_pizza_places(self):
    pizza_place_presenters = []
    for pizza_place in self.meetup.pizza_places.all():
      pizza_place_presenters.append(PizzaPlacePresenter(pizza_place, YelpApi))
    return pizza_place_presenters



