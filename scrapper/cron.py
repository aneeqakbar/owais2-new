from datetime import datetime
import os
from django.conf import settings
import pandas as pd
from django.utils.timezone import make_aware
from apscheduler.schedulers.background import BackgroundScheduler
from .models import AnalyticalValue, ScraperData

def int_or_none(value):
    try:
        return int(value)
    except:
        return None

def fetch_telegram_data(code = None):
    print('fetching telegram started')
    sheet_id = "194uUksIX6_qQ27RcgZ01hggRHV3ZFCcPBiF5PBn_6P4"
    # sheet_name = "Sheet1"
    tab_id = "0"
    # url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_id}"
    data_frame = pd.read_csv(url)

    print(f"Got {len(data_frame)} Entries")

    data_instances_created = []
    data_instances_exists = []
    for i in range(len(data_frame)):
        cryptocurrency = data_frame["Cryptocurrency"][i]
        ticker = data_frame["Ticker"][i]
        yesterday_total = data_frame["YESTERDAY_TOTAL"][i]
        today_total = data_frame["TODAY_TOTAL"][i]
        difference = data_frame["Difference"][i]
        yesterday_icospeaks = data_frame["yesterday_icospeaks"][i]
        today_icospeaks = data_frame["today_icospeaks"][i]
        yesterday_cryptocom = data_frame["yesterday_cryptocom"][i]
        today_cryptocom = data_frame["today_cryptocom"][i]
        yesterday_coinmarket = data_frame["yesterday_coinmarket"][i]
        today_coinmarket = data_frame["today_coinmarket"][i]
        date = data_frame["DATE"][i]

        year = date.split(' ')[0].split('-')[0]
        month = date.split(' ')[0].split('-')[1]
        day = date.split(' ')[0].split('-')[2]
        hour = date.split(' ')[1].split(':')[0]
        minute = date.split(' ')[1].split(':')[1]
        second = date.split(' ')[1].split(':')[2]

        data_created = True
        try:
            data = ScraperData.objects.get(
                scraper_name = "T",
                cryptocurrency = cryptocurrency,
                ticker = ticker,
                code = code,
            )
            data_created = False
        except:
            data = ScraperData(
                scraper_name = "T",
                cryptocurrency = cryptocurrency,
                ticker = ticker,
                code = code,
            )

        if data_created:
            data_instances_created.append(data)
        else:
            data_instances_exists.append(data)
        print("processed #",i)

    ScraperData.objects.bulk_create(data_instances_created)
    # ScraperData.objects.bulk_update(data_instances_exists, fields=[
    #     "scraper_name",
    #     "ticker",
    #     "cryptocurrency",
    # ])

    analytical_values_created = []
    analytical_values_exists = []
    for i in range(len(data_frame)):
        cryptocurrency = data_frame["Cryptocurrency"][i]
        ticker = data_frame["Ticker"][i]
        yesterday_total = data_frame["YESTERDAY_TOTAL"][i]
        today_total = data_frame["TODAY_TOTAL"][i]
        difference = data_frame["Difference"][i]
        yesterday_icospeaks = data_frame["yesterday_icospeaks"][i]
        today_icospeaks = data_frame["today_icospeaks"][i]
        yesterday_cryptocom = data_frame["yesterday_cryptocom"][i]
        today_cryptocom = data_frame["today_cryptocom"][i]
        yesterday_coinmarket = data_frame["yesterday_coinmarket"][i]
        today_coinmarket = data_frame["today_coinmarket"][i]
        date = data_frame["DATE"][i]

        year = date.split(' ')[0].split('-')[0]
        month = date.split(' ')[0].split('-')[1]
        day = date.split(' ')[0].split('-')[2]
        hour = date.split(' ')[1].split(':')[0]
        minute = date.split(' ')[1].split(':')[1]
        second = date.split(' ')[1].split(':')[2]

        values_created = True
        data = ScraperData.objects.get(
            scraper_name = "T",
            cryptocurrency = cryptocurrency,
            ticker = ticker,
            code = code,
        )

        try:
            analytical_value = AnalyticalValue.objects.get(
                data = data,
                created_at = make_aware(datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))),
            )
            values_created = False
        except:
            analytical_value = AnalyticalValue(
                data = data,
                created_at = make_aware(datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))),
            )

        analytical_value.yesterday_total = int_or_none(yesterday_total)
        analytical_value.today_total = int_or_none(today_total)
        analytical_value.difference = int_or_none(difference)
        analytical_value.yesterday_icospeaks = int_or_none(yesterday_icospeaks)
        analytical_value.today_icospeaks = int_or_none(today_icospeaks)
        analytical_value.yesterday_cryptocom = int_or_none(yesterday_cryptocom)
        analytical_value.today_cryptocom = int_or_none(today_cryptocom)
        analytical_value.yesterday_coinmarket = int_or_none(yesterday_coinmarket)
        analytical_value.today_coinmarket = int_or_none(today_coinmarket)

        if values_created:
            analytical_values_created.append(analytical_value)
        else:
            analytical_values_exists.append(analytical_value)
        print("analytics #",i)

    AnalyticalValue.objects.bulk_update(analytical_values_exists, fields=[
        "yesterday_total",
        "today_total",
        "difference",
        "yesterday_icospeaks",
        "today_icospeaks",
        "yesterday_cryptocom",
        "today_cryptocom",
        "yesterday_coinmarket",
        "today_coinmarket",
    ])
    AnalyticalValue.objects.bulk_create(analytical_values_created)

    print('fetching telegram Stoped')

def fetch_reddit_data():
    print('fetching reddit started')
    sheet_id = "194uUksIX6_qQ27RcgZ01hggRHV3ZFCcPBiF5PBn_6P4"
    # sheet_name = "Sheet1"
    tab_id = "1216468972"
    # url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={tab_id}"
    data_frame = pd.read_csv(url)

    print(f"Got {len(data_frame)} Entries")

    data_instances_created = []
    data_instances_exists = []
    for i in range(len(data_frame)):
        cryptocurrency = data_frame["Cryptocurrency"][i]
        ticker = data_frame["Ticker"][i]
        yesterday_total = data_frame["YESTERDAY_TOTAL"][i]
        today_total = data_frame["TODAY_TOTAL"][i]
        difference = data_frame["Difference"][i]
        date = data_frame["DATE"][i]

        year = date.split(' ')[0].split('-')[0]
        month = date.split(' ')[0].split('-')[1]
        day = date.split(' ')[0].split('-')[2]
        hour = date.split(' ')[1].split(':')[0]
        minute = date.split(' ')[1].split(':')[1]
        second = date.split(' ')[1].split(':')[2]

        data_created = True
        try:
            data = ScraperData.objects.get(
                scraper_name = "R",
                cryptocurrency = cryptocurrency,
                ticker = ticker,
                code = "",
            )
            data_created = False
        except:
            data = ScraperData(
                scraper_name = "R",
                cryptocurrency = cryptocurrency,
                ticker = ticker,
                code = "",
            )

        if data_created:
            data_instances_created.append(data)
        else:
            data_instances_exists.append(data)
        print("processed #",i)

    ScraperData.objects.bulk_create(data_instances_created)

    analytical_values_created = []
    analytical_values_exists = []
    for i in range(len(data_frame)):
        cryptocurrency = data_frame["Cryptocurrency"][i]
        ticker = data_frame["Ticker"][i]
        yesterday_total = data_frame["YESTERDAY_TOTAL"][i]
        today_total = data_frame["TODAY_TOTAL"][i]
        difference = data_frame["Difference"][i]
        date = data_frame["DATE"][i]

        year = date.split(' ')[0].split('-')[0]
        month = date.split(' ')[0].split('-')[1]
        day = date.split(' ')[0].split('-')[2]
        hour = date.split(' ')[1].split(':')[0]
        minute = date.split(' ')[1].split(':')[1]
        second = date.split(' ')[1].split(':')[2]

        values_created = True
        data = ScraperData.objects.get(
            scraper_name = "R",
            cryptocurrency = cryptocurrency,
            ticker = ticker,
            code = "",
        )

        try:
            analytical_value = AnalyticalValue.objects.get(
                data = data,
                created_at = make_aware(datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))),
            )
            values_created = False
        except:
            analytical_value = AnalyticalValue(
                data = data,
                created_at = make_aware(datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))),
            )

        analytical_value.yesterday_total = int_or_none(yesterday_total)
        analytical_value.today_total = int_or_none(today_total)
        analytical_value.difference = int_or_none(difference)

        if values_created:
            analytical_values_created.append(analytical_value)
        else:
            analytical_values_exists.append(analytical_value)
        print("analytics #",i)

    AnalyticalValue.objects.bulk_update(analytical_values_exists, fields=[
        "yesterday_total",
        "today_total",
        "difference",
        "yesterday_icospeaks",
        "today_icospeaks",
        "yesterday_cryptocom",
        "today_cryptocom",
        "yesterday_coinmarket",
        "today_coinmarket",
    ])
    AnalyticalValue.objects.bulk_create(analytical_values_created)

    print('fetching reddit Stoped')


def start_cron():
    scheduler = BackgroundScheduler()
    # fetch_telegram_data()
    # scheduler.add_job(fetch_telegram_data, 'interval', minutes=5)
    scheduler.start()