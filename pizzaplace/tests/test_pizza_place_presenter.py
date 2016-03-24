from django.test import TestCase

from unittest.mock import patch

from pizzaplace.models import PizzaPlace
from pizzaplace.presenter.pizza_place_presenter import PizzaPlacePresenter


class TestPizzaPlacePresenter(TestCase):

  def setUp(self):
    self.patcher = patch('pizzaplace.services.yelp_api')
    self.mock_yelp_api = self.patcher.start()
    self.mock_yelp_api.return_value.get_response.return_value.json.return_value = {'rating' : 5}
    self.pizza_place = PizzaPlace(name='Oh Pizza!', yelp_url='https://www.yelp.com/biz/lombardis-pizza-new-york')

  def test_yelp_presenter_returns_yelp_url(self):
    presenter = PizzaPlacePresenter(self.pizza_place, self.mock_yelp_api)
    self.assertEquals(presenter.yelp_url(), 'https://www.yelp.com/biz/lombardis-pizza-new-york')

  def test_yelp_presenter_returns_business_name(self):
    presenter = PizzaPlacePresenter(self.pizza_place, self.mock_yelp_api)
    self.assertEquals(presenter.pizza_place_name(), 'Oh Pizza!')

  def test_yelp_presenter_returns_yelp_review(self):
    presenter = PizzaPlacePresenter(self.pizza_place, self.mock_yelp_api)
    self.assertEquals(presenter.pizza_place_rating(), "🍕🍕🍕🍕🍕")

  def test_yelp_presenter_rounds_yelp_review_down(self):
    self.mock_yelp_api.return_value.get_response.return_value.json.return_value = {'rating' : 4.5}
    presenter = PizzaPlacePresenter(self.pizza_place, self.mock_yelp_api)
    self.assertEquals(presenter.pizza_place_rating(), "🍕🍕🍕🍕")

  def test_yelp_presenter_rounds_yelp_review_down(self):
    self.mock_yelp_api.return_value.get_response.return_value.json.return_value = {}
    presenter = PizzaPlacePresenter(self.pizza_place, self.mock_yelp_api)
    self.assertEquals(presenter.pizza_place_rating(), "No Rating")

  def tearDown(self):
    self.addCleanup(self.patcher.stop)
