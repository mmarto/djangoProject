from django.core.management.base import BaseCommand, CommandError
from reportsViewer.models import Category, Report, UserReport
from django.contrib.auth.models import User
import os, shutil, sys, getpass
# from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

class Command(BaseCommand):
    
    def handle(self, *args, **options):
#        data = {}
#        title = input('Please enter report title: ')
#        if not title:
#            self.stdout.write('Title is empty.\nExiting with error!')
#            sys.exit(1)
#        if Report.objects.filter(title=title).exists():
#            print('Warning; The report with title {} already exists!'.format(title))
#            update = input('Would you like to update it? (yes/no) (default no): ')
#            update = update.strip().lower()
#            if update == 'yes':
#                update = 'yes'
#            else:
#                sys.exit(1)
#                
#        data['title'] = title
#        file = input('Path to report: ')
#        file = os.path.expanduser(file)
#        file = os.path.abspath(file)
#        if not os.path.isfile(file):
#            self.stdout.write('{}\nFile does not exist or is not readable.\nExiting with error!'.format(file))
#            sys.exit(1)
#        data['size'] = os.path.getsize(file)
#        
#        username = getpass.getuser()
#        inputUsername = input('Please enter user (default {}): '.format(username))
#        inputUsername = inputUsername or username
#        data['creator'] = inputUsername
#
#        self.stdout.write('Report Categories')
#        # self.stdout.write('{:>5}: {}'.format('Id', 'Category'))
#        categories = Category.objects.all()
#        for category in categories:
#            self.stdout.write('{:>5}: {}'.format(category.id, category.name))
#        catId = input('Please enter a category id: ')
#        try:
#            catId = int(catId)
#        except ValueError:
#            self.stdout.write('The category id is not a number.\nExiting with error!')
#            sys.exit(1)
#        if not Category.objects.filter(id=catId).exists():
#            self.stdout.write('Category does not exist.\nExiting with error!')
#            sys.exit(1)
#        inputUsers = input('Please enter list of users (comma separated): ') 
#        users = [i.strip() for i in inputUsers.split(',')]
#        existingUsers = User.objects.all()
#        existingUsersList = [users.username for users in User.objects.all()]
#        for user in users:
#            if user not in existingUsersList:
#                self.stdout.write('{} does not exist.\nExiting with error!')
#                sys.exit(1)
#        
#        #for user in users:
#            #print(existingUsers.filter(username=user))
#
#        self.stdout.write('Please enter a comment: ')
#        sentinel = ''
#        comment = '\n'.join(iter(input, sentinel))
#        data['comment'] = comment
#        print('Report Type')
#        for choice in ('P', 'Already Generated Report'), ('R', 'Real Time Manually Generated Report'):
#            print('{0:>5}: {1}'.format(*choice))
#        reportType = input('Please choose report type (default P): ')
#        reportType = reportType or 'P'
#        data['type'] = reportType
#        data['pub_date'] = timezone.now()
#        cat = Category.objects.get(id=catId)
#        data['category'] = cat
#        categoryDir = cat.dir
#        newFile = '{0}/{1}'.format(categoryDir, os.path.basename(file))
#        data['path'] = newFile
#        try:
#            #os.rename(file,newFile)
#            shutil.move(file,newFile)
#        except:
#            raise
#        print('Creating or updating a database entry...')
#        report, created = Report.objects.get_or_create(title=title, defaults=data)
#        if created:
#            self.stdout.write('Report published successfully!')
#        else:
#            Report.objects.update(**data)
#        print('Done!')
#        #sys.exit(1)
#        print('Setting up report user permissions...')
#        for user in users:
#            reportUser = User.objects.get(username=user)
#            #if UserReport.objects.get(report_id=report.id,user_id=reportUser.id).exists():
#            #    print('userreport exists')
#            #else:
#            #    print('userreport does not exist')
#            #userReport, created = UserReport.objects.get_or_create(report_id=report.id,user_id=reportUser.id)
#            userReport, created = UserReport.objects.get_or_create(report=report,user=reportUser)
#            self.stdout.writei('{0} - done.'(userReport))
#        print('Done!')
        #mail = EmailMessage('Test Sending Email From Django', '<b>It worked...</b>', 'django@mail',['mhristov@mail'])
        mail = EmailMultiAlternatives(subject='Test Sending Email From Django', body='It worked...', from_email='django@mail',to=['mhristov@mail'], alternatives=(('<b>It worked...</b>','text/html'),))
        mail.attach_file('/home/users/mhristov/ibcs/data/reportsViewer/customer_weekly_reports_by_country/Weekly_Activity_Report_China_20150209.pdf')
        mail.send()
