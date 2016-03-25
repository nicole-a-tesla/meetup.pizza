import datetime

from django.utils.timezone import make_aware

from meetup.services import map_url_generator
from pizzaplace.services.yelp_service import YelpService

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
    return map_url_generator.generate_google_url(lat, lon)

  def meetup_pizza_places(self):
    pizza_places = self.meetup.pizza_places.all()
    pizza_place_presenters = [YelpService(place).get_decorated_pizza_place() for place in pizza_places]
    return pizza_place_presenters
