# Generated by Django 5.0.4 on 2024-05-15 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0002_remove_listing_state_remove_listing_zipcode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_inbusiness',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ListingReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.EmailField(max_length=255)),
                ('review', models.TextField(blank=True, null=True)),
                ('vote', models.IntegerField(choices=[(1, 'Awful'), (2, 'Bad'), (3, 'Medium'), (4, 'Good'), (5, 'Great')], default=3)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Purchasing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.EmailField(max_length=255)),
                ('months', models.SmallIntegerField(blank=True, null=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listing.listing')),
            ],
        ),
    ]