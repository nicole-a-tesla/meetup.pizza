class ParsedMeetupResponse():
  def __init__(self, raw_parsed_response):
    self.raw_parsed_response = raw_parsed_response

  @property
  def venue(self):
    return self.raw_parsed_response['venue']

  @property
  def next_event_topic(self):
    return self.raw_parsed_response['next_event_topic']

  @property
  def datetime(self):
    return self.raw_parsed_response['datetime']

  @property
  def lat(self):
    return self.raw_parsed_response['lat']

  @property
  def lon(self):
    return self.raw_parsed_response['lon']
