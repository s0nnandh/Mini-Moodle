# Generated by Django 3.1.4 on 2020-12-08 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bogs', '0016_auto_20201208_1720'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='message_seen',
            unique_together={('form2', 'person')},
        ),
    ]
