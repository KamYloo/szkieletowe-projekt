from django import template
from django.contrib.auth.models import Group
import os

register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value)

@register.filter
def filepath(value):
    return str(value).split("media")[1].replace("\\","//")

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False