import re

def calculate_change(new, old):
    return (new-old) / old *100

def get_number(value):
    return re.sub("[^0-9.+-]", '', str(value))