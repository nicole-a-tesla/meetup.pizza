class ParsedYelpResponse():
  def __init__(self, raw_parsed_response):
    self.raw_parsed_response = raw_parsed_response

  @property
  def rating(self):
      return self.raw_parsed_response.get('rating')
