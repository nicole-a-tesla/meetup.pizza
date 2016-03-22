from meetuppizza.settings import base

class MeetupClient():

  def build_api_components(self, meetup_link):
    url = self.build_api_url(meetup_link)
    params = self.build_params()
    return {'url': url, 'params': params}

  def get_unique_id(self, meetup_link):
    return meetup_link.split('/')[-2]

  def build_api_url(self, meetup_link):
    return "https://api.meetup.com/" + self.get_unique_id(meetup_link) + '/events'


  def build_params(self):
    return {"key": base.MEETUP_KEY }

