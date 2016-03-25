from django.test import TestCase


from pizzaplace.models import PizzaPlace
from pizzaplace.presenter.pizza_place_presenter import PizzaPlacePresenter
from pizzaplace.services.parsed_yelp_response import ParsedYelpResponse

class TestPizzaPlacePresenter(TestCase):

  def setUp(self):
    self.pizza_place = PizzaPlace(name='Oh Pizza!', yelp_url='https://www.yelp.com/biz/lombardis-pizza-new-york')

  def test_yelp_presenter_returns_yelp_url(self):
    raw_yelp_response = {'rating': 4}
    parsed_yelp_response = ParsedYelpResponse(raw_yelp_response)
    presenter = PizzaPlacePresenter(self.pizza_place, parsed_yelp_response)
    self.assertEquals(presenter.yelp_url(), 'https://www.yelp.com/biz/lombardis-pizza-new-york')

  def test_yelp_presenter_returns_business_name(self):
    raw_yelp_response = {'rating': 4}
    parsed_yelp_response = ParsedYelpResponse(raw_yelp_response)
    presenter = PizzaPlacePresenter(self.pizza_place, parsed_yelp_response)
    self.assertEquals(presenter.pizza_place_name(), 'Oh Pizza!')

  def test_yelp_presenter_returns_yelp_review(self):
    raw_yelp_response = {'rating': 5}
    parsed_yelp_response = ParsedYelpResponse(raw_yelp_response)
    presenter = PizzaPlacePresenter(self.pizza_place, parsed_yelp_response)
    self.assertEquals(presenter.pizza_place_rating(), "🍕🍕🍕🍕🍕")

  def test_yelp_presenter_rounds_yelp_review_down(self):
    raw_yelp_response = {'rating': 4.5}
    parsed_yelp_response = ParsedYelpResponse(raw_yelp_response)
    presenter = PizzaPlacePresenter(self.pizza_place, parsed_yelp_response)
    self.assertEquals(presenter.pizza_place_rating(), "🍕🍕🍕🍕")

  def test_yelp_presenter_returns_no_rating(self):
    raw_yelp_response = {}
    parsed_yelp_response = ParsedYelpResponse(raw_yelp_response)
    presenter = PizzaPlacePresenter(self.pizza_place, parsed_yelp_response)
    self.assertEquals(presenter.pizza_place_rating(), "No Rating")
