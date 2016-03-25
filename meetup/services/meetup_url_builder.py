from django.conf import settings

class MeetupUrlBuilder():
  def __init__(self, meetup_url):
    self.meetup_url = meetup_url

  def get_unique_id(self):
    return self.meetup_url.split('/')[-2]

  def build_api_url(self):
    return "https://api.meetup.com/" + self.get_unique_id() + '/events'

  def build_authorization_components(self):
    return {'params': {"key": settings.MEETUP_KEY }}
