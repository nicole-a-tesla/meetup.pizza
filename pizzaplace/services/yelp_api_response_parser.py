class YelpApiResponseParser():
  def __init__(self, response):
    self.response = response.json()

  def parse(self):
    return {'rating': self.response.get('rating')}
