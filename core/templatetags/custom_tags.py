import re

import markdown
import pytz
from django import template

register = template.Library()

@register.filter
def day_in_bahasa(value):
    days = {
        'sunday': 'Minggu',
        'monday': 'Senin',
        'tuesday': 'Selasa',
        'wednesday': 'Rabu',
        'thursday': 'Kamis',
        'friday': 'Jumat',
        'saturday': 'Sabtu'
    }
    return days[value.lower()]

@register.filter
def month_in_bahasa(value):
    months = {
        'january': 'Januari',
        'february': 'Februari',
        'march': 'Maret',
        'april': 'April',
        'may': 'Mei',
        'june': 'Juni',
        'july': 'Juli',
        'august': 'Agustus',
        'september': 'September',
        'october': 'Oktober',
        'november': 'November',
        'december': 'Desember'
    }
    return months[value.lower()]

@register.filter
def show_file_name(value):
    value = value.split('/')[1]
    return value

@register.simple_tag()
def as_timezone(time_input, timezone, format=None):
    if not format:
        format = '%Y-%m-%d %H:%M'
    timezone = pytz.timezone(timezone)
    res = time_input.astimezone(timezone).strftime(format)
    return res

@register.filter
def remove_dash(value):
    return str(value).replace('-', '')


@register.filter
def render_markdown(text):
    html = markdown.markdown(text)
    html = html.replace('<h1>', '<h1 class="mb-4">')
    html = html.replace('<h2>', '<h2 class="mb-4">')
    html = html.replace('<h3>', '<h3 class="mb-4">')
    html = html.replace('<h4>', '<h4 class="mb-4">')
    html = html.replace('<h5>', '<h5 class="mb-4">')
    html = html.replace('<h6>', '<h6 class="mb-4">')
    html = html.replace('<ol>', '<ol class="mb-4">')
    html = re.sub(r'<li>\s*<p>\s*<strong>', '<li><p class="mt-4"><strong>', html)
    return html

@register.filter
def total_respondent(angket_session):
    return angket_session.responses.all().values('session').distinct().count()

@register.filter
def datetime_as_timezone(time_input, timezone):
    timezone = pytz.timezone(timezone)
    res = time_input.astimezone(timezone)
    return res

@register.filter
def middle(a, b):
    return int((a + b) / 2)

@register.filter
def get_percent(value, total):
    res = (value-1) / (total-1) * 100
    if res > 0:
        if res < 50:
            return res - 0.3
        elif res == 50:
            return res - .4
        else:
            return res - 0.8
    return res

@register.filter
def in_range(value, start=0):
    return range(start, value+1)