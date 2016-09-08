import os
from django.core.management.base import BaseCommand, CommandError
from reportsViewer.models import Report, Category, UserReport
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = {}
        title = 'Dummy Report Title {}'
        filename = '{}/dummy_report_filename_{}'
        cat = Category.objects.get(id=1)
        creator = 'mhristov'
        comment = 'Dummy comment {}'
        pup_date = timezone.now()
        reportUser = User.objects.get(username='mhristov')
        type = 'P'

        for i in range(500):
            data['title'] = title.format(i)
            fullpath = filename.format(cat.dir, i)
            data['path'] = fullpath
            with open(fullpath, mode='w') as f:
                print(fullpath, file=f)
            data['category'] = cat
            data['creator'] = creator
            data['pub_date'] = pup_date
            data['comment'] = comment.format(i)
            data['size'] = os.path.getsize(fullpath)
            data['type'] = type
            report = Report.objects.create(**data)
            userReport, created = UserReport.objects.get_or_create(report=report, user=reportUser)
            print(report)
            print(userReport)
