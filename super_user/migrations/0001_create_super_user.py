from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.models import User
import os

def migrate_up(apps, schema_editor):
  db_alias = schema_editor.connection.alias
  User.objects.create_superuser('adminotaur', 'admin@meetup.pizza', os.getenv('ADMIN_PASS'))

def migrate_down(apps, schema_editor):
  db_alias = schema_editor.connection.alias
  User.objects.using(db_alias).filter(username="adminotaur", is_superuser = True).delete()

class Migration(migrations.Migration):

  dependencies = [
      ('auth', '0007_alter_validators_add_error_messages'),
  ]

  operations = [
    migrations.RunPython(migrate_up, migrate_down),
  ]