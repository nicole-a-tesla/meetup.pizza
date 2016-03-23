from meetup.services.meetup_presenter import MeetupPresenter
from meetup.services.meetup_client import MeetupClient

class MeetupService():
  def __init__(self, meetup):
    self.meetup = meetup

  def get_decorated_meetup(self):
    meetup_data = MeetupClient(self.meetup.meetup_url).get_meetup_info()
    return MeetupPresenter(self.meetup, meetup_data)
