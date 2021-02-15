# Generated by Django 3.1.6 on 2021-02-15 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exehubapp', '0007_auto_20210215_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_group_admin', models.BooleanField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exehubapp.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exehubapp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exehubapp.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exehubapp.user')),
            ],
        ),
    ]
