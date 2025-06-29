from django import template
import re

register = template.Library()

@register.filter
def email_to_id(email):
    return re.sub(r'[^a-zA-Z0-9]', '-', email)
