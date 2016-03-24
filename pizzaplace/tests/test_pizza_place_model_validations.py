from django.test import TestCase
from django.core.exceptions import ValidationError

from pizzaplace.models import PizzaPlace

class TestPizzaPlaceModelValidations(TestCase):
  def setUp(self):
    self.invalid_url_format_message = "Url should be in form 'https://www.yelp.com/biz/some-pizza-place'"

  def test_error_raised_on_nonsense_url(self):
    pizza_place = PizzaPlace(name="Name", yelp_url="not.a/url?")
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      pizza_place.full_clean()

  def test_error_raised_if_not_a_yelp_url(self):
    pizza_place = PizzaPlace(name="Name", yelp_url="http://notyelpatall.com/biz/prince-st-pizza-new-york")
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      pizza_place.full_clean()

  def test_error_raised_if_no_corresponding_business_on_yelp(self):
    pizza_place = PizzaPlace(name="Name", yelp_url="http://yelp.com/biz/not-a-real-business")
    with self.assertRaisesRegexp(ValidationError, 'Yelp Business not found on Yelp.com'):
      pizza_place.full_clean()

  def test_error_raised_if_no_bizname_in_pizza_place_url(self):
    pizza_place = PizzaPlace(name="Oh Pizza!", yelp_url='https://www.yelp.com/biz/')
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      pizza_place.full_clean()

  def test_error_raised_if_no_biz_key_in_pizza_place_url(self):
    pizza_place = PizzaPlace(name="Oh Pizza!", yelp_url='https://www.yelp.com/prince-st-pizza-new-york')
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      pizza_place.full_clean()

  def test_no_error_raised_if_url_contains_search_query_params(self):
    pizza_place = PizzaPlace(name="Oh Pizza!", yelp_url='https://www.yelp.com/biz/lombardis-pizza-new-york?osq=lombardis-pizza-new-york')
    errors_raised_by_pizza_place = pizza_place.full_clean()
    self.assertIsNone(errors_raised_by_pizza_place)

  def test_error_raised_if_url_doesnt_contain_valid_business_name(self):
    pizza_place = PizzaPlace(name="Oh Pizza!", yelp_url='https://www.yelp.com/biz/imaginary-pizza/')
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      pizza_place.full_clean()

  def test_no_error_raised_if_url_contains_no_search_query_params(self):
    pizza_place = PizzaPlace(name="Oh Pizza!", yelp_url='https://www.yelp.com/biz/lombardis-pizza-new-york')
    errors_raised_by_pizza_place = pizza_place.full_clean()
    self.assertIsNone(errors_raised_by_pizza_place)

  def test_error_raised_if_url_has_multiple_biznames(self):
    pizza_place = PizzaPlace(name="Oh Pizza!", yelp_url='https://www.yelp.com/biz/lombardis-pizza-new-york/some-other-stuff')
    with self.assertRaisesRegexp(ValidationError, self.invalid_url_format_message):
      pizza_place.full_clean()

