from meetup.presenter.meetup_presenter import MeetupPresenter
from meetup.services.meetup_client import MeetupClient
from meetup.services.parsed_meetup_response import ParsedMeetupResponse

class MeetupService():
  def __init__(self, meetup):
    self.meetup = meetup

  def get_decorated_meetup(self):
    meetup_data = MeetupClient(self.meetup.meetup_url).get_meetup_info()
    parsed_data_object = ParsedMeetupResponse(meetup_data)
    return MeetupPresenter(self.meetup, parsed_data_object)
