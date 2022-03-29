# Generated by Django 4.0.3 on 2022-03-28 15:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScraperData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scraper_name', models.CharField(choices=[('T', 'Telegram'), ('R', 'Reddit')], max_length=255)),
                ('cryptocurrency', models.CharField(max_length=255)),
                ('ticker', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnalyticalValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yesterday_total', models.IntegerField(default=0, null=True)),
                ('today_total', models.IntegerField(default=0, null=True)),
                ('difference', models.IntegerField(default=0, null=True)),
                ('yesterday_icospeaks', models.IntegerField(default=0, null=True)),
                ('today_icospeaks', models.IntegerField(default=0, null=True)),
                ('yesterday_cryptocom', models.IntegerField(default=0, null=True)),
                ('today_cryptocom', models.IntegerField(default=0, null=True)),
                ('yesterday_coinmarket', models.IntegerField(default=0, null=True)),
                ('today_coinmarket', models.IntegerField(default=0, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2022, 3, 28, 20, 25, 38, 602339))),
                ('data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='analytical_values', to='scrapper.scraperdata')),
            ],
        ),
    ]