from meetup.models import Meetup
from meetup.services.meetup_presenter import MeetupPresenter
from meetup.services.meetup_client import MeetupClient

class MeetupService():
  def __init__(self, meetup):
    self.meetup = meetup

  def get_decorated_meetup(self):
    parsed_response = MeetupClient(self.meetup.meetup_link).get_meetup_info()
    return MeetupPresenter(self.meetup, parsed_response)
