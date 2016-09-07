from django.core.management.base import BaseCommand, CommandError
from reportsViewer.models import Report, Category, UserReport
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {}
        title = 'Dummy Report Title {}'
        filename = 'dummy_report_filename_{}'
        cat = Category.objects.get(id=1)
        creator = 'mhristov'
        comment = 'Dummy comment {}'
        pup_date = timezone.now()
        size = '{}'
        type = 'P'

        for i in range(500):
            data['title'] = title.format(i)
            data['path'] = filename.format(i)
            data['category'] = cat
            data['creator'] = creator
            data['pub_date'] = pup_date
            data['comment'] = comment.format(i)
            data['size'] = size.format(i)
            data['type'] = type
            ret = Report.objects.create(**data)
            print(ret)
