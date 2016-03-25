from pizzaplace.presenter.pizza_place_presenter import PizzaPlacePresenter
from pizzaplace.services.yelp_client import YelpClient
from pizzaplace.services.parsed_yelp_response import ParsedYelpResponse

class YelpService():
  def __init__(self, pizza_place):
    self.pizza_place = pizza_place

  def get_decorated_pizza_place(self):
    yelp_data = YelpClient(self.pizza_place.yelp_url).get_yelp_info()
    parsed_data_object = ParsedYelpResponse(yelp_data)
    return PizzaPlacePresenter(self.pizza_place, parsed_data_object)
