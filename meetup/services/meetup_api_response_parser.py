def parse(api_response):
  parsed_response = {}
  parsed_response['venue'] = api_response.get(0).get('venue').get('name')
  parsed_response['next_event_topic'] = api_response.get(0).get('name')
  parsed_response['datetime'] = api_response.get(0).get('time')
  parsed_response['lat'] = api_response.get(0).get('group').get('lat')
  parsed_response['lon'] = api_response.get(0).get('group').get('lon')
  return parsed_response
