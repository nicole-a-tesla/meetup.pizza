from django.test import TestCase
from pizzaplace.models import PizzaPlace
from django.db import IntegrityError
from django.db import DataError
import pdb

class TestPizzaPlace(TestCase):

  def test_pizza_is_real(self):
    pizza_place = PizzaPlace()
    self.assertIsInstance(pizza_place, PizzaPlace)

  def test_creation_of_pizza_place_with_name(self):
    pizza_place = PizzaPlace(name="Pete Zazz")
    self.assertEquals(pizza_place.name, "Pete Zazz")

  def test_name_must_be_unique(self):
    place1 = PizzaPlace(name="Such Pizza")
    place1.save()
    place2 = PizzaPlace(name="Such Pizza")
    self.assertRaises(IntegrityError, place2.save)

  def test_string_representation(self):
    place = PizzaPlace(name="Pete's aPlace")
    self.assertEquals("Pete's aPlace", str(place))

  def test_name_length(self):
    name = "x" * 501
    place = PizzaPlace(name=name)
    self.assertRaises(DataError, place.save)

  def test_name_can_not_be_blank(self):
    place = PizzaPlace()
    self.assertRaises(IntegrityError, place.save)