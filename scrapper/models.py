from django.db import models
import datetime

from scrapper.utils import calculate_change, get_number

# Create your models here.


class ScrapperOutput_withNumbers(models.Model):
    userid= models.CharField(max_length=50)
    links= models.TextField()
    Name= models.TextField()
    Price= models.CharField(max_length=100)
    Kilometers= models.CharField(max_length=100)
    Date= models.TextField()
    Power= models.TextField()
    Image= models.TextField()
    Number= models.TextField()
    def __str__(self):
        return self.Name

class ScrapperOutput_withoutNumbers(models.Model):
    userid= models.CharField(max_length=50)
    links= models.TextField()
    Name= models.TextField()
    Price= models.TextField()
    Kilometers= models.TextField()
    Date= models.TextField()
    Power= models.TextField()
    Image= models.TextField()
    def __str__(self):
        return self.Name






class AnalyticalValue(models.Model):
    data = models.ForeignKey("scrapper.ScraperData", on_delete=models.CASCADE, related_name="analytical_values", null=True, blank=True)
    yesterday_total = models.IntegerField(default=0, null=True)
    today_total = models.IntegerField(default=0, null=True)
    difference = models.IntegerField(default=0, null=True)
    yesterday_icospeaks = models.IntegerField(default=0, null=True)
    today_icospeaks = models.IntegerField(default=0, null=True)
    yesterday_cryptocom = models.IntegerField(default=0, null=True)
    today_cryptocom = models.IntegerField(default=0, null=True)
    yesterday_coinmarket = models.IntegerField(default=0, null=True)
    today_coinmarket = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=False, default=datetime.datetime.now())


class ScraperData(models.Model):
    FIELDS = [
        "yesterday_total",
        "today_total",
        "difference",
        "yesterday_icospeaks",
        "today_icospeaks",
        "yesterday_cryptocom",
        "today_cryptocom",
        "yesterday_coinmarket",
        "today_coinmarket",
    ]
    SCRAPER_NAMES = (
        ('T', 'Telegram'),
        ('R', 'Reddit'),
    )
    SHEET_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
    )

    scraper_name = models.CharField(max_length=255, choices=SCRAPER_NAMES)
    cryptocurrency = models.CharField(max_length=255)
    ticker = models.CharField(max_length=50)
    code = models.CharField(max_length=50, choices=SHEET_CHOICES)
    date = models.DateTimeField(auto_now_add=True, null=True)


    def get_field(self, field_name=''):
        if not field_name or not field_name in self.FIELDS:
            return 0
        return self.analytical_values.all().order_by("-created_at").values_list(field_name, flat=True).first()

    def get_field_analytics(self, field_name=''):

        if not field_name or not field_name in self.FIELDS:
            return {
                "daily": 0,
                "weekly": 0,
                "yearly": 0,
            }

        current_time = datetime.datetime.now()

        min_delta = datetime.timedelta(days=365)
        max_delta = datetime.timedelta(days=365*2)
        previous_datas = self.analytical_values.filter(created_at__range = [current_time - max_delta, current_time - min_delta]).values_list(field_name, flat=True)
        current_datas = self.analytical_values.filter(created_at__range = [current_time - min_delta, current_time]).values_list(field_name, flat=True)

        previous_value = 0
        for value in previous_datas:
            previous_value += float(get_number(value))
        current_value = 0
        for value in current_datas:
            current_value += float(get_number(value))
        try:
            previous_value = previous_value / len(previous_datas)
            current_value = current_value / len(current_datas)
            yearly = calculate_change(current_value, previous_value)
        except ZeroDivisionError:
            yearly = 0

        min_delta = datetime.timedelta(weeks=1)
        max_delta = datetime.timedelta(weeks=2)
        previous_datas = self.analytical_values.filter(created_at__range = [current_time - max_delta, current_time - min_delta]).values_list(field_name, flat=True)
        current_datas = self.analytical_values.filter(created_at__range = [current_time - min_delta, current_time]).values_list(field_name, flat=True)

        previous_value = 0
        for value in previous_datas:
            previous_value += float(get_number(value))
        current_value = 0
        for value in current_datas:
            current_value += float(get_number(value))
        try:
            previous_value = previous_value / len(previous_datas)
            current_value = current_value / len(current_datas)
            weekly = calculate_change(current_value, previous_value)
        except ZeroDivisionError:
            weekly = 0

        min_delta = datetime.timedelta(days=1)
        max_delta = datetime.timedelta(days=2)
        previous_datas = self.analytical_values.filter(created_at__range = [current_time - max_delta, current_time - min_delta]).values_list(field_name, flat=True)
        current_datas = self.analytical_values.filter(created_at__range = [current_time - min_delta, current_time]).values_list(field_name, flat=True)
        previous_value = 0
        for value in previous_datas:
            previous_value += float(get_number(value))
        current_value = 0
        for value in current_datas:
            current_value += float(get_number(value))
        try:
            previous_value = previous_value / len(previous_datas)
            current_value = current_value / len(current_datas)
            daily = calculate_change(current_value, previous_value)
        except ZeroDivisionError:
            daily = 0

        return {
            "daily": daily,
            "weekly": weekly,
            "yearly": yearly,
        }


    def get_chart_data(self, field_name="", days=7):
        if not field_name or not field_name in self.FIELDS:
            return {
                "labels": [],
                "data": []
            }

        chart_data = {
            "labels": [],
            "data": []
        }

        current_time = datetime.datetime.now()
        analytical_values = self.analytical_values.all()
        indexes = int(days)
        for i in range(indexes):
            max_delta = current_time - datetime.timedelta(days=(indexes-1)-i)
            min_delta = current_time - datetime.timedelta(days=(indexes-1)-i+1)

            value = analytical_values.filter(created_at__range = [min_delta, max_delta]).values_list(field_name, flat=True).first()
            if not value:
                value = 0
            # for value in values:
            #     sum += float(get_number(value))
            chart_data['data'].append(f'{value}')
            chart_data['labels'].append(f'Day {i+1}')
        return chart_data
