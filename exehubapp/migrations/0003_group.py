# Generated by Django 3.1.6 on 2021-02-15 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exehubapp', '0002_auto_20210215_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=45)),
                ('group_owner', models.CharField(max_length=45)),
                ('group_email', models.CharField(max_length=45)),
                ('group_irc', models.CharField(max_length=45)),
                ('fee', models.FloatField()),
            ],
        ),
    ]
