from django.test import TestCase, Client
from django.contrib.auth.models import User
from meetuppizza.forms import RegistrationForm
from django.contrib import auth

import pdb

params = {
      'username':'Bjorn',
      'email':'bjorn@bjorn.com',
      'password1':'bjornbjorn',
      'password2':'bjornbjorn'
    }

class TestLandingPage(TestCase):

  def test_landing_page_is_there(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)

  def test_landing_page_contains_pizza(self):
    response = self.client.get('/')
    self.assertContains(response, "pizza")

  def test_signup_redirects_to_landing_page(self):
    response = self.client.post('/sign_up', params, follow=True)
    self.assertRedirects(response, '/')

  def test_signed_in_user_email_displayed_on_home_page(self):
    self.client.post('/sign_up', params)
    response = self.client.get('/')
    self.assertContains(response, "bjorn@bjorn.com")


class TestUserAuthentication(TestCase):

  def test_user_is_created_on_signup(self):
    self.client.post('/sign_up', params)
    user = User.objects.get(username='Bjorn')
    self.assertIsNotNone(user)


  def test_user_is_logged_in_after_signup(self):
    self.client.post('/sign_up', params)
    user = User.objects.get(username='Bjorn')
    self.assertFalse(user.is_anonymous())

  def test_user_is_anonyoous_after_log_out(self):
    self.client.post('/sign_up', params)
    self.client.get('/sign_out')
    user = auth.get_user(self.client)
    self.assertTrue(user.is_anonymous())

  def test_user_is_not_anonymous_after_login(self):
    self.client.post('/sign_up', params)
    self.client.get('/sign_out')
    login_params = {
      'username':'Bjorn',
      'password':'bjornbjorn',
    }
    self.client.post('/sign_in', login_params)
    user = auth.get_user(self.client)
    self.assertFalse(user.is_anonymous())

  def test_user_is_anonymous_if_login_is_invalid(self):
    login_params = {
      'username':'Birds',
      'password':'argulonic',
    }
    self.client.post('/sign_in', login_params)
    user = auth.get_user(self.client)
    self.assertTrue(user.is_anonymous())
