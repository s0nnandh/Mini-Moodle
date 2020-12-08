# Generated by Django 3.1.4 on 2020-12-08 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bogs', '0015_auto_20201208_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bogs.person', to_field='userid'),
        ),
        migrations.AlterField(
            model_name='message_seen',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bogs.person', to_field='userid'),
        ),
    ]