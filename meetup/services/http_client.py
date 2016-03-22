import requests

class HttpClient():
  def get_response(url_components):
    url = url_components['url']
    params = url_components['params']
    return requests.get(url, params=params)


