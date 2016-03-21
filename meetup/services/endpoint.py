import requests

class Endpoint():
  def get_response(url, params={}):
    return requests.get(url, params=params)


