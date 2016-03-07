from django.test import TestCase
from django.contrib.auth.models import User


class TestSuperUser(TestCase):

  def test_super_user_is_created_and_is_super(self):
    user = User.objects.get(username='adminotaur')
    self.assertTrue(user.is_staff)
    self.assertTrue(user.is_superuser)

  def test_super_user_is_created_with_hashed_password(self):
    user = User.objects.get(username='adminotaur')
    self.assertIn('pbkdf2_sha256$', user.password)
