from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.hashers import make_password
import os

def migrate_up(apps, schema_editor):
  User = apps.get_model('auth', 'User')
  db_alias = schema_editor.connection.alias
  User.objects.using(db_alias).create(
    username='adminotaur',
    email='admin@meetup.pizza',
    password=make_password(os.getenv('ADMIN_PASS')),
    is_superuser=True,
    is_staff=True
  )

def migrate_down(apps, schema_editor):
  User = apps.get_model('auth', 'User')
  db_alias = schema_editor.connection.alias
  User.objects.using(db_alias).filter(username="adminotaur", is_superuser=True).delete()

class Migration(migrations.Migration):

  dependencies = [
      ('auth', '0007_alter_validators_add_error_messages'),
  ]

  operations = [
    migrations.RunPython(migrate_up, migrate_down),
  ]