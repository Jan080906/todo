# Generated by Django 3.2.12 on 2022-02-27 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0007_task_sequence'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='last_modified_when',
            new_name='last_updated',
        ),
    ]