# Generated by Django 2.2.5 on 2022-01-18 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='photo',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room'),
        ),
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(blank=True, to='rooms.Amenity'),
        ),
        migrations.AddField(
            model_name='room',
            name='facilities',
            field=models.ManyToManyField(blank=True, to='rooms.Facility'),
        ),
        migrations.AddField(
            model_name='room',
            name='house_rules',
            field=models.ManyToManyField(blank=True, to='rooms.HouseRule'),
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rooms.RoomType'),
        ),
    ]
