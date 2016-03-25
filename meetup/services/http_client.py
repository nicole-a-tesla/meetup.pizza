import requests

class HttpClient():

  def get_response(url, url_components):
    return requests.get(url, **url_components)
