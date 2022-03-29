from django import template
import re

register = template.Library()

def compareInt(value, arg):
    """Compares number event if they are strings"""
    try:
        value = re.sub("[^0-9.+-]", '', str(value))
        arg = re.sub("[^0-9.+-]", '', str(arg))
        n1 = float(value)
        n2 = float(arg)
        return n1 > n2
    except:
        return None

register.filter('compareInt', compareInt)

def at_index(data, index):
    """gets value at index"""
    try:
        return data[int(index)]
    except:
        return None

register.filter('at_index', at_index)

def sum_number(num1, num2):
    """Sums the numbers"""
    try:
        return int(float(num1) + float(num2))
    except:
        return None

register.filter('sum_number', sum_number)

def get_field(data, field):
    """gets analytics of a field"""
    return data.get_field(field)

register.filter('get_field', get_field)

def get_field_analytics(data, field):
    """gets analytics of a field"""
    return data.get_field_analytics(field)

register.filter('get_field_analytics', get_field_analytics)

def get_field_cart_data(data, field):
    """gets chart data for 7 days of a field"""
    return data.get_chart_data(field_name=field, days=7)

register.filter('get_field_cart_data', get_field_cart_data)