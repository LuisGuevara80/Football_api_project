# Generated by Django 5.0.8 on 2024-08-19 19:50

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=3, null=True)),
                ('flag_url', models.URLField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('type', models.CharField(max_length=50)),
                ('logo_url', models.URLField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_data.country')),
            ],
            options={
                'ordering': ['country', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('current', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='football_data.league')),
            ],
            options={
                'ordering': ['-year'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('code', models.CharField(blank=True, max_length=3, null=True)),
                ('founded', models.IntegerField(blank=True, null=True)),
                ('national', models.BooleanField(default=False)),
                ('logo_url', models.URLField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_data.country')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('firstname', models.CharField(blank=True, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('birth_place', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_country', models.CharField(blank=True, max_length=100, null=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('height', models.CharField(blank=True, max_length=10, null=True)),
                ('weight', models.CharField(blank=True, max_length=10, null=True)),
                ('injured', models.BooleanField(blank=True, null=True)),
                ('photo_url', models.URLField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='football_data.team')),
            ],
            options={
                'ordering': ['lastname', 'firstname'],
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(max_length=100)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('surface', models.CharField(max_length=50)),
                ('image_url', models.URLField()),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='venue', to='football_data.team')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('referee', models.CharField(blank=True, max_length=100, null=True)),
                ('time_zone', models.CharField(max_length=50)),
                ('date', models.DateTimeField(db_index=True)),
                ('timestamp', models.IntegerField()),
                ('status_long', models.CharField(max_length=50)),
                ('status_short', models.CharField(max_length=2)),
                ('status_elapsed', models.IntegerField(blank=True, null=True)),
                ('round', models.CharField(max_length=50)),
                ('goals_home', models.IntegerField(blank=True, null=True)),
                ('goals_away', models.IntegerField(blank=True, null=True)),
                ('score_halftime_home', models.IntegerField(blank=True, null=True)),
                ('score_halftime_away', models.IntegerField(blank=True, null=True)),
                ('score_fulltime_home', models.IntegerField(blank=True, null=True)),
                ('score_fulltime_away', models.IntegerField(blank=True, null=True)),
                ('score_extratime_home', models.IntegerField(blank=True, null=True)),
                ('score_extratime_away', models.IntegerField(blank=True, null=True)),
                ('score_penalty_home', models.IntegerField(blank=True, null=True)),
                ('score_penalty_away', models.IntegerField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixtures', to='football_data.league')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixtures', to='football_data.season')),
                ('team_away', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_fixtures', to='football_data.team')),
                ('team_home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_fixtures', to='football_data.team')),
                ('venue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fixtures', to='football_data.venue')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
