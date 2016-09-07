from django import template
from django.template.defaultfilters import stringfilter
from reportsViewer.models import Category, Report
import os

register = template.Library()

@register.inclusion_tag('reportsViewer/cats.html', takes_context=True)
def get_category_list(context,cat=None):
    request = context['request']
    category_list = list()
    for category in Category.objects.order_by('name'):
        cnt = Report.objects.filter(category=category, type='P', users__id=request.user.id).count()
        if cnt > 0:
            category_list.append(category)
    return {'cats': Category.objects.filter(name__in=category_list), 'act_cat': cat}

@register.filter(name='basename')
@stringfilter
def basename(value):
    return os.path.basename(value)
