
def get_nested_venue_attr_or_default(json, nested_attr):
  venue = json[0].get('venue')

  if venue:
    return venue.get(nested_attr)
  else:
    return "No %s listed" %nested_attr


def parse(api_response):
  json = api_response.json()
  parsed_response = {}

  if json:
    parsed_response['venue'] = get_nested_venue_attr_or_default(json, 'name')
    parsed_response['lat'] = get_nested_venue_attr_or_default(json, 'lat')
    parsed_response['lon'] = get_nested_venue_attr_or_default(json, 'lon')
    parsed_response['next_event_topic'] = json[0].get('name', 'No topic listed')
    parsed_response['datetime'] = json[0].get('time', 'No time listed')
  return parsed_response
