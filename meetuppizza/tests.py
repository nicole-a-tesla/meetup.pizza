from django.test import TestCase

class Test(TestCase):
  def test_landing_page_is_there(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
