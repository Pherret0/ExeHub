# Generated by Django 3.1.6 on 2021-02-15 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exehubapp', '0003_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='group_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exehubapp.group'),
            preserve_default=False,
        ),
    ]
