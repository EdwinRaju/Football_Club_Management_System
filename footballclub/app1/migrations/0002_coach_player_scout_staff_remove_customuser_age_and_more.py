# Generated by Django 4.2.7 on 2024-02-20 00:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('cdate', models.DateField(blank=True, null=True)),
                ('sal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('img', models.ImageField(blank=True, default='', null=True, upload_to='uploads')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('pos', models.CharField(blank=True, max_length=50, null=True)),
                ('jno', models.IntegerField(blank=True, null=True)),
                ('cdate', models.DateField(blank=True, null=True)),
                ('sal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('img', models.ImageField(blank=True, default='', null=True, upload_to='uploads')),
            ],
        ),
        migrations.CreateModel(
            name='Scout',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('cdate', models.DateField(blank=True, null=True)),
                ('sal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('img', models.ImageField(blank=True, default='', null=True, upload_to='uploads')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('cdate', models.DateField(blank=True, null=True)),
                ('sal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('img', models.ImageField(blank=True, default='', null=True, upload_to='uploads')),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='age',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='cdate',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='img',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='jno',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='pos',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='sal',
        ),
        migrations.RemoveField(
            model_name='match',
            name='time',
        ),
        migrations.AlterField(
            model_name='match',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.venue'),
        ),
        migrations.CreateModel(
            name='ScoutedPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('sal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('position', models.CharField(choices=[('CF', 'Forward'), ('CM', 'Midfielder'), ('CD', 'Defender'), ('GK', 'Goal Keeper')], max_length=50)),
                ('current_status', models.CharField(choices=[('Free', 'Free'), ('club', 'In a Club')], max_length=10)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('email', models.EmailField(max_length=254)),
                ('scout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.scout')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerDetailsRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('sal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('position', models.CharField(choices=[('CF', 'Forward'), ('CM', 'Midfielder'), ('CD', 'Defender'), ('GK', 'Goal Keeper')], max_length=50)),
                ('current_status', models.CharField(choices=[('Free', 'Free'), ('club', 'In a Club')], max_length=10)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('email', models.EmailField(max_length=254)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.scoutedplayer')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='app1.player')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='app1.player')),
            ],
        ),
        migrations.CreateModel(
            name='CoachRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=50)),
                ('min_age', models.IntegerField()),
                ('max_age', models.IntegerField()),
                ('min_rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('max_rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.coach')),
            ],
        ),
        migrations.AlterField(
            model_name='playerperformance',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.player'),
        ),
        migrations.AlterField(
            model_name='trainingsession',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.coach'),
        ),
    ]
