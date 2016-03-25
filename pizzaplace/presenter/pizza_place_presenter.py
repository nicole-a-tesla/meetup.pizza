class PizzaPlacePresenter():
  def __init__(self, pizza_place, parsed_response):
    self.pizza_place = pizza_place
    self.parsed_response = parsed_response

  def yelp_url(self):
    return self.pizza_place.yelp_url

  def pizza_place_name(self):
    return self.pizza_place.name

  def pizza_place_rating(self):
    rating = self.parsed_response.rating
    if rating:
      return int(rating) * "🍕"
    return 'No Rating'

