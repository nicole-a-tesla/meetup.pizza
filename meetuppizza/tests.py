from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
import pdb


class Test(TestCase):
  # def test_landing_page_is_there(self):
  #   response = self.client.get('/')
  #   self.assertEqual(response.status_code, 200)

  # def test_page_contains_pizza(self):
  #   response = self.client.get('/')
  #   self.assertContains(response, "pizza")

  # def test_page_contains_signup(self):
  #   response = self.client.get('/')
  #   self.assertContains(response, "Sign Up")

  # def test_signup_redirects(self):
  #   params =  {'email':'bjorn@bjorn.com', 'password':'bjorn'}

  #   response = self.client.post('/sign_up', params, follow=True)
  #   self.assertRedirects(response, '/welcome')

  # def test_user_is_created(self):
  #   params =  {'email':'bjorn@bjorn.com', 'password':'bjorn'}
  #   c = Client()
  #   c.post('/sign_up', params)
  #   self.assertEqual(1, len(User.objects.all()))

  def test_email_displayed_on_welcome_page(self):
    params =  {'email':'bjorn@bjorn.com', 'password':'bjorn'}
    c = Client()
    c.post('/sign_up', params)
    response = c.get('/welcome')
    self.assertContains(response, "bjorn@bjorn.com")

