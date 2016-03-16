def parse(api_response):
  json = api_response.json()
  parsed_response = {}

  if json:
    parsed_response['venue'] = json[0].get('venue').get('name')
    parsed_response['next_event_topic'] = json[0].get('name')
    parsed_response['datetime'] = json[0].get('time')
    parsed_response['lat'] = json[0].get('group').get('lat')
    parsed_response['lon'] = json[0].get('group').get('lon')
  return parsed_response
