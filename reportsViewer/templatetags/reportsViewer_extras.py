from django import template
from django.template.defaultfilters import stringfilter
from reportsViewer.models import Category
import os

register = template.Library()

@register.inclusion_tag('reportsViewer/cats.html')
def get_category_list():
    return {'cats': Category.objects.all()}

@register.filter(name='basename')
@stringfilter
def basename(value):
    return os.path.basename(value)
