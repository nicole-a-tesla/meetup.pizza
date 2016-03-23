class MeetupApiResponseParser():
  def __init__(self, http_response):
    self.http_response = http_response

  @property
  def json(self):
    return self.http_response.json()[0]

  def extract_attribute(self, context, *args):
    current_key = args[0]
    not_found_message = "No %s listed" %current_key
    value_at_current_key = context.get(current_key, not_found_message)

    if self.exit_condition_is_true(context, args):
      return value_at_current_key

    return self.extract_attribute(value_at_current_key, args[1])

  def exit_condition_is_true(self, dic, args):
    this_is_the_last_arg = len(args) == 1
    no_matching_element_found = dic.get(args[0]) == None
    return this_is_the_last_arg or no_matching_element_found

  def parse(self):
    if self.json:
      return {
        'venue'           : self.extract_attribute(self.json, 'venue', 'name'),
        'lat'             : self.extract_attribute(self.json, 'venue', 'lat'),
        'lon'             : self.extract_attribute(self.json, 'venue', 'lon'),
        'next_event_topic': self.extract_attribute(self.json, 'name'),
        'datetime'        : self.extract_attribute(self.json, 'time')
      }
