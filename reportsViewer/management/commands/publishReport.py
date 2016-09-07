from django.core.management.base import BaseCommand, CommandError
from reportsViewer.models import Category, Report, UserReport
from django.contrib.auth.models import User, Group
import os, shutil, sys, getpass
# from datetime import datetime
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.db import connection

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        data = {}
        emailData = {}
        title = input('Please enter report title: ')
        if not title:
            self.stdout.write('Title is empty.\nExiting with error!')
            sys.exit(1)
        if Report.objects.filter(title=title).exists():
            print('Warning; The report with title {} already exists!'.format(title))
            update = input('Would you like to update it? Yes/No (default No): ')
            update = update.strip().lower()
            if update == 'yes':
                update = 'yes'
            else:
                sys.exit(1)
                
        #data['title'] = title
        emailData['subject'] = 'Reports Viewer: {}'.format(title)
        file = input('Path to report: ')
        file = os.path.expanduser(file)
        file = os.path.abspath(file)
        if not os.path.isfile(file):
            self.stdout.write('{}\nFile does not exist or is not readable.\nExiting with error!'.format(file))
            sys.exit(1)
        data['size'] = os.path.getsize(file)
        
        print('Report Type')
        for choice in ('P', 'Already Generated Report'), ('R', 'Real Time Manually Generated Report'):
            print('{0:>5}: {1}'.format(*choice))
        reportType = input('Please choose report type (default P): ')
        reportType = reportType or 'P'

        if reportType == 'R' and not file.endswith('.rptdesign'):
            self.stdout.write('Looks like {} is not a BIRT report (*.rptdesign). Only BIRT is supported for real time report generation.\nExiting with error!'.format(file))
        
        username = getpass.getuser()
        inputUsername = input('Please enter from user (default {}): '.format(username))
        inputUsername = inputUsername or username
        creatorUser = User.objects.filter(username=inputUsername)
        if not creatorUser.exists():
            self.stdout.write('User {} does not exists in reportsViewer database.\nExiting with error!'.format(inputUsername))
            sys.exit(1)
        data['creator'] = inputUsername
        emailData['from_email'] = creatorUser.get().email

        self.stdout.write('Report Categories')
        # self.stdout.write('{:>5}: {}'.format('Id', 'Category'))
        categories = Category.objects.all()
        for category in categories:
            self.stdout.write('{:>5}: {}'.format(category.id, category.name))
        catId = input('Please enter a category id: ')
        try:
            catId = int(catId)
        except ValueError:
            self.stdout.write('The category id is not a integer.\nExiting with error!')
            sys.exit(1)
        if not Category.objects.filter(id=catId).exists():
            self.stdout.write('Category does not exist.\nExiting with error!')
            sys.exit(1)
        users = list()
        inputGroupsQuestion = input('Would you like to publish to a group of users? Yes/No (default No): ')
        if inputGroupsQuestion.lower() == 'yes':
            self.stdout.write('Available User Groups')
            groups = Group.objects.all().order_by('id')
            for group in groups:
                self.stdout.write('{:>5}: {}'.format(group.id, group.name))
            groupId = input('Please enter a group id: ')
            try:
                groupId = int(groupId)
            except ValueError:
                self.stdout.write('The group id is not an integer.\nExiting with error!')
                sys.exit(1)
            users = [u.username for u in User.objects.filter(groups__id = groupId)]
        else:
            inputUsers = input('Please enter list of users (comma separated): ') 
            users = [i.strip() for i in inputUsers.split(',')]
            existingUsers = User.objects.all()
            existingUsersList = [users.username for users in User.objects.all()]
            for user in users:
                if user not in existingUsersList:
                    self.stdout.write('{} does not exist.\nExiting with error!'.format(user))
                    sys.exit(1)
        
        #for user in users:
        #    print(user)
        #sys.exit()

        self.stdout.write('Please enter a comment: ')
        sentinel = ''
        comment = '\n'.join(iter(input, sentinel))
        data['comment'] = comment

        data['type'] = reportType
        data['pub_date'] = timezone.now()
        attach = False
        if data['type'] == 'P':
            attachQuestion = input('Would you like to attach the report to the email? Yes/No (default No): ')
            if attachQuestion.strip().lower() == 'yes':
                attach = True
        cat = Category.objects.get(id=catId)
        data['category'] = cat
        categoryDir = cat.dir
        categoryBirtDir = cat.birt_dir

        newFile = '{0}/{1}'.format(categoryDir, os.path.basename(file)) if data['type'] == 'P' else '{0}/{1}'.format(categoryBirtDir, os.path.basename(file))

        try:
            #os.rename(file,newFile)
            shutil.move(file,newFile)
        except:
            raise
        data['path'] = newFile
        print('Creating or updating a database entry...')
        report, created = Report.objects.get_or_create(title=title, defaults=data)
        if created:
            self.stdout.write('Report published successfully!')
        else:
            #data['title'] = title
            report.__dict__.update(data)
            report.save()
        print('Done!')
        emailComment = self.constructEmailBody(report, comment)
        emailData['body'] = strip_tags(emailComment)
        emailData['alternatives'] = ((emailComment,'text/html'),)
        #sys.exit(1)
        print('Setting up report user permissions...')
        usersEmails = []
        for user in users:
            reportUser = User.objects.get(username=user)
            usersEmails.append(reportUser.email)
            #if UserReport.objects.get(report_id=report.id,user_id=reportUser.id).exists():
            #    print('userreport exists')
            #else:
            #    print('userreport does not exist')
            #userReport, created = UserReport.objects.get_or_create(report_id=report.id,user_id=reportUser.id)
            userReport, created = UserReport.objects.get_or_create(report=report,user=reportUser)
            self.stdout.write('{0} - done.'.format(userReport))
        emailData['to'] = usersEmails
        print('Done!')
        print('Sending email...')
        #mail = EmailMessage('Test Sending Email From Django', '<b>It worked...</b>', 'django@mail',['mhristov@mail'])
        #mail = EmailMultiAlternatives(subject='Test Sending Email From Django', body='It worked...', from_email='django@mail',to=['mhristov@mail'], alternatives=(('<b>It worked...</b>','text/html'),))
        mail = EmailMultiAlternatives(**emailData)
        if attach:
            mail.attach_file(data['path'])
        mail.send()
        print('Done!')

    def constructEmailBody(self, report, comment):
        html = '''<!DOCTYPE html>
                  <html lang="en">
                  <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head>
                  <h3>{0}</h3>
                  <div>{1}</div>
                  Report details: <a href='http://localhost:8000/reportsViewer/report/{2}/'>http://localhost:8000/reportsViewer/report/{2}/</a><br />
                  Direct download link: <a href='http://localhost:8000/reportsViewer/download_report/{2}/'>http://localhost:8000/reportsViewer/download_report/{2}/</a>
                  </html>
         '''.format(report.title, comment, report.id )
        return html
