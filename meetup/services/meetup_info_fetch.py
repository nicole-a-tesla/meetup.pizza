from django.db import models
from meetup.services.meetup_api_lookup_agent import MeetupApiLookupAgent
import time
import pdb

class MeetupInfoFetch():
  def __init__(self, meetups, lookup_agent):
    self.lookup_agent = lookup_agent
    self.meetups = meetups

  def fat_meetups(self):
    new_meetups = []

    for meetup in self.meetups:
      event_info = self.lookup_meetup_info(meetup)

      if event_info:
        self.append_info_to_meetup(meetup, event_info)

    return self.meetups

  def lookup_meetup_info(self, meetup):
    lookup_agent_instance = self.lookup_agent(meetup.meetup_link)
    return lookup_agent_instance.get_response('events').json()

  def append_info_to_meetup(self, meetup, event_info):
      meetup.venue = event_info[0]['venue']['name']
      meetup.next_event_topic = event_info[0]['name']
      meetup.datetime = self.parse_time(event_info[0]['time'])
      meetup.map_link = self.generate_map_link(event_info)


  def parse_time(self, time_string):
    return time.ctime(int(time_string))[:-6]

  def generate_map_link(self, event_info):
    lat = event_info[0]['group']['lat']
    lon = event_info[0]['group']['lon']
    return "https://www.google.com/maps?q=%s,%s" % (lat, lon)
