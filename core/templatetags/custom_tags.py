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