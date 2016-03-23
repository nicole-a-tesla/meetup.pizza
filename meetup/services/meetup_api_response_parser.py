class MeetupApiResponseParser():
  def __init__(self, http_response):
    self.http_response = http_response

  @property
  def json(self):
    return self.http_response.json()[0]

  # def get_nested_attribute(self, nested_attr):
  #   venue = self.json[0].get('venue')

  #   if venue:
  #     return venue.get(nested_attr)
  #   else:
  #     return "No %s listed" %nested_attr

  def extract_attribute(self, dic, *args):
    find_this = args[0]
    not_found_message = "No %s listed" %find_this

    if len(args) == 1 or dic.get(find_this) == None:   # Or there's nothing at venue
      return dic.get(find_this, not_found_message)

    new_dic = dic.get(find_this, not_found_message)
    return self.extract_attribute(new_dic, args[1])


  def parse(self):
    if self.json:
      return {
        'venue': self.extract_attribute(self.json, 'venue', 'name'),
        'lat' : self.extract_attribute(self.json, 'venue', 'lat'),
        'lon' : self.extract_attribute(self.json, 'venue', 'lon'),
        'next_event_topic': self.extract_attribute(self.json, 'name'),
        'datetime': self.extract_attribute(self.json, 'time')
      }
