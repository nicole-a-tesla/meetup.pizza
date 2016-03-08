from django.db import models
from meetup.services.meetup_api_lookup_agent import MeetupApiLookupAgent
import time
import pdb

class MeetupInfoFetch():
  def __init__(self, meetups): 
    self.meetups = meetups

  def fat_meetups(self):
    new_meetups = []

    for meetup in self.meetups:
      event_info = self.lookup_meetup_info(meetup)

      if event_info:
        self.append_info_to_meetup(meetup, event_info)

    return self.meetups

  def lookup_meetup_info(self, meetup):
    lookup_agent = MeetupApiLookupAgent(meetup.meetup_link)
    return lookup_agent.get_response('events').json()

  def append_info_to_meetup(self, meetup, event_info):
      meetup.venue = event_info[0]['venue']['name']
      meetup.next_event_topic = event_info[0]['name']
      meetup.datetime = self.parse_time(event_info[0]['time'])

  def parse_time(self, time_string):
    return time.ctime(int(time_string))[:-6]
