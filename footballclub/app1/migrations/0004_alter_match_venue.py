# Generated by Django 4.2.7 on 2024-02-17 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_trainingsession_coach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.venue'),
        ),
    ]
