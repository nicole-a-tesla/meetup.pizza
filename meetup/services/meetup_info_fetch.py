from django.db import models
from meetup.services.meetup_api_lookup_agent import MeetupApiLookupAgent
import time

class FetchMeetupInfo():
  def __init__(self, meetups, lookup_agent):
    self.lookup_agent = lookup_agent
    self.meetups = meetups

  def fat_meetups(self):
    new_meetups = []

    for meetup in self.meetups:
      event_info = self.lookup_meetup_info(meetup)

      new_meetup = self.build_meetup_info_dictionary(meetup, event_info)
      new_meetups.append(new_meetup)

    return new_meetups

  def lookup_meetup_info(self, meetup):
    lookup_agent_instance = self.lookup_agent(meetup.meetup_link)
    return lookup_agent_instance.get_response('events').json()

  def convert_meetup_object_to_dictionary(self, meetup):
    new_meetup = {}
    new_meetup['name'] = meetup.name
    new_meetup['meetup_link'] = meetup.meetup_link
    new_meetup['pizza_places'] = meetup.pizza_places.all()
    return new_meetup


  def build_meetup_info_dictionary(self, meetup, event_info):
      new_meetup = self.convert_meetup_object_to_dictionary(meetup)

      if event_info:
        new_meetup['venue'] = event_info[0]['venue']['name']
        new_meetup['next_event_topic'] = event_info[0]['name']
        new_meetup['datetime'] = self.parse_time(event_info[0]['time'])
        new_meetup['map_link'] = self.generate_map_link(event_info)

      return new_meetup


  def parse_time(self, time_string):
    return time.ctime(int(time_string))[:-6]

  def generate_map_link(self, event_info):
    lat = event_info[0]['group']['lat']
    lon = event_info[0]['group']['lon']
    return "https://www.google.com/maps?q=%s,%s" % (lat, lon)
