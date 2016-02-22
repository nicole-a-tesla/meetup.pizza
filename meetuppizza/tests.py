from django.test import TestCase

class Test(TestCase):
  def test_landing_page_is_there(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)

  def test_page_contains_pizza(self):
    response = self.client.get('/')
    self.assertContains(response, "pizza")
