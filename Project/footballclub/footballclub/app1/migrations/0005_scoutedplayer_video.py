# Generated by Django 4.2.7 on 2024-04-17 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_injury_scanning_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoutedplayer',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]