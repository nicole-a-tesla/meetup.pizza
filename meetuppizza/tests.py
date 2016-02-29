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
    c = Client()
    c.post('/sign_up', self.params)
    self.assertEqual(1, len(User.objects.all()))


  def test_user_is_logged_in_after_signup(self):
    c = Client()
    c.post('/sign_up', self.params)
    user = User.objects.get(username='Bjorn')
    self.assertFalse(user.is_anonymous())

  def test_email_displayed_on_home_page(self):
    c = Client()
    c.post('/sign_up', self.params)
    response = c.get('/')
    self.assertContains(response, "bjorn@bjorn.com")

  def test_user_log_out(self):
    client = Client()
    client.post('/sign_up', self.params)
    client.get('/sign_out')
    user = auth.get_user(client)
    self.assertTrue(user.is_anonymous())

  def test_login(self):
    c = Client()
    c.post('/sign_up', self.params)
    c.get('/sign_out')
    login_params = {
      'username':'Bjorn', 
      'password':'bjornbjorn',     
    }
    c.post('/sign_in', login_params)
    user = auth.get_user(c)
    self.assertFalse(user.is_anonymous())

  def test_invalid_login(self):
    c = Client()
    c.post('/sign_up', self.params)
    c.get('/sign_out')
    login_params = {
      'username':'Birds', 
      'password':'argulonic',     
    }
    c.post('/sign_in', login_params)
    user = auth.get_user(c)
    self.assertTrue(user.is_anonymous())



