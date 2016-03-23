class GenericApi():
  BASE_URL = ''

  def __init__(self, url):
    self.url = url

  def get_response(self):
    pass

  def build_api_url(self):
    pass

  def exists(self):
    return self.get_response().status_code == 200

  def get_unique_id(self):
    pass
