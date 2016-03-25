from django.test import TestCase
from django.db import DataError
from django.db import IntegrityError

from pizzaplace.models import PizzaPlace


class TestPizzaPlace(TestCase):

  def setUp(self):
    self.prince_street_pizza_url = 'https://www.yelp.com/biz/prince-st-pizza-new-york'
    self.pizza_name1 = 'Such Pizza'

  def test_pizza_is_real(self):
    pizza_place = PizzaPlace()
    self.assertIsInstance(pizza_place, PizzaPlace)

  def test_creation_of_pizza_place_with_name(self):
    pizza_place = PizzaPlace(name=self.pizza_name1, yelp_url=self.prince_street_pizza_url)
    self.assertEquals(pizza_place.name, self.pizza_name1)

  def test_name_must_be_unique(self):
    PizzaPlace.objects.create(name=self.pizza_name1, yelp_url=self.prince_street_pizza_url)
    place2 = PizzaPlace(name=self.pizza_name1, yelp_url='https://www.yelp.com/biz/lombardis-pizza-new-york')
    self.assertRaises(IntegrityError, place2.save)

  def test_url_must_be_unique(self):
    PizzaPlace.objects.create(name="Much Pizza", yelp_url=self.prince_street_pizza_url)
    place2 = PizzaPlace(name=self.pizza_name1, yelp_url=self.prince_street_pizza_url)
    self.assertRaises(IntegrityError, place2.save)

  def test_string_representation_of_pizza_place(self):
    place = PizzaPlace(name=self.pizza_name1, yelp_url=self.prince_street_pizza_url)
    self.assertEquals(self.pizza_name1, str(place))

  def test_name_length_invalid_if_over_500_char(self):
    name = "x" * 501
    place = PizzaPlace(name=name, yelp_url=self.prince_street_pizza_url)
    self.assertRaises(DataError, place.save)

  def test_raises_error_if_name_is_blank(self):
    place = PizzaPlace(yelp_url=self.prince_street_pizza_url)
    self.assertRaises(IntegrityError, place.save)

  def test_raises_error_if_url_is_blank(self):
    place = PizzaPlace(name=self.pizza_name1)
    self.assertRaises(IntegrityError, place.save)
