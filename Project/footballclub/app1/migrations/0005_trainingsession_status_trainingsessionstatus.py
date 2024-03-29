# Generated by Django 4.2.6 on 2023-11-07 07:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_rename_id_trainingsession_training_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingsession',
            name='status',
            field=models.CharField(choices=[('unfinished', 'Unfinished'), ('finished', 'Finished')], default='unfinished', max_length=10),
        ),
        migrations.CreateModel(
            name='TrainingSessionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shoot', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('passing', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('dribble', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('defense', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('physical', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('speed', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('status', models.CharField(choices=[('unfinished', 'Unfinished'), ('finished', 'Finished')], default='unfinished', max_length=10)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('training_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.trainingsession')),
            ],
        ),
    ]
