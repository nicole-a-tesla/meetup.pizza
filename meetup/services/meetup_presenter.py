import time

class MeetupPresenter():
  def __init__(self, meetup, api_response_info):
    self.meetup = meetup
    self.api_response_info = api_response_info

  def get_meetup_link(self):
    return self.meetup.meetup_link

  def get_meetup_name(self):
    return self.meetup.name

  def get_meetup_venue(self):
    return self.api_response_info['venue']

  def get_meetup_next_event_topic(self):
    return self.api_response_info.get('next_event_topic')

  def get_meetup_datetime(self):
    time_string = self.api_response_info['datetime']
    return time.ctime(int(time_string))[:-6]

  def get_meetup_map_link(self):
    lat = self.api_response_info['lat']
    lon = self.api_response_info['lon']
    return "https://www.google.com/maps?q=%s,%s" % (lat, lon)

  def get_meetup_pizza_places(self):
    return self.meetup.pizza_places.all()

