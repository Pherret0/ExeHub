# Generated by Django 3.1.6 on 2021-02-15 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exehubapp', '0005_auto_20210215_2232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='group_id',
            new_name='group',
        ),
    ]
