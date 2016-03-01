from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from meetuppizza.forms import RegistrationForm
from django.contrib import auth

import pdb


class Test(TestCase):
  def setUp(self):
    self.params =  {
      'username':'Bjorn',
      'email':'bjorn@bjorn.com',
      'password1':'bjornbjorn',
      'password2':'bjornbjorn'
    }

    self.client = Client()

  def test_landing_page_is_there(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)

  def test_page_contains_pizza(self):
    response = self.client.get('/')
    self.assertContains(response, "pizza")

  def test_signup_redirects(self):
    response = self.client.post('/sign_up', self.params, follow=True)
    self.assertRedirects(response, '/')

  def test_user_is_created(self):
    self.client.post('/sign_up', self.params)
    user = User.objects.get(username='Bjorn')
    self.assertFalse(user == None)

  def test_user_is_logged_in_after_signup(self):
    self.client.post('/sign_up', self.params)
    user = User.objects.get(username='Bjorn')
    self.assertFalse(user.is_anonymous())

  def test_email_displayed_on_home_page(self):
    self.client.post('/sign_up', self.params)
    response = self.client.get('/')
    self.assertContains(response, "bjorn@bjorn.com")

  def test_user_log_out(self):
    self.client.post('/sign_up', self.params)
    self.client.get('/sign_out')
    user = auth.get_user(self.client)
    self.assertTrue(user.is_anonymous())

  def test_login(self):
    self.client.post('/sign_up', self.params)
    self.client.get('/sign_out')
    login_params = {
      'username':'Bjorn',
      'password':'bjornbjorn',
    }
    self.client.post('/sign_in', login_params)
    user = auth.get_user(self.client)
    self.assertFalse(user.is_anonymous())

  def test_invalid_login(self):
    login_params = {
      'username':'Birds',
      'password':'argulonic',
    }
    self.client.post('/sign_in', login_params)
    user = auth.get_user(self.client)
    self.assertTrue(user.is_anonymous())



