def parse(api_response):
  json = api_response.json()
  parsed_response = {}

  if json:

    try:
      parsed_response['venue'] = json[0].get('venue').get('name')
    except AttributeError:
      parsed_response['venue'] = "No venue listed"

    try:
      parsed_response['next_event_topic'] = json[0].get('name')
    except AttributeError:
      parsed_response['next_event_topic'] = "No name listed"

    try:
      parsed_response['datetime'] = json[0].get('time')
    except AttributeError:
      parsed_response['datetime'] = "No time listed"

    try:
      parsed_response['lat'] = json[0].get('venue').get('lat')
      parsed_response['lon'] = json[0].get('venue').get('lon')
    except AttributeError:
      parsed_response['lat'] = '40.689745'
      parsed_response['lon'] = '-74.0476567'

  return parsed_response
