# Generated by Django 5.0.4 on 2024-05-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_useraccount_address_useraccount_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='experience',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='facebook_account',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='linkedin_account',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='twitter_account',
            field=models.URLField(blank=True, null=True),
        ),
    ]