import os, re
import errno
from django.db import models
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify
from datetime import datetime
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(unique=True)
    dir = models.CharField(max_length=1500, unique=True)
    birt_dir = models.CharField(max_length=1500, unique=True)
    archive_dir = models.CharField(max_length=1500, unique=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.slug = slug
        dir = '{0}/{1}'.format(settings.REPORTS_DIR, re.sub('-', '_', slug))
        birtDir = '{0}/birt/{1}'.format(settings.REPORTS_DIR, re.sub('-', '_', slug))
        archiveDir = '{0}/archive/{1}'.format(settings.REPORTS_DIR, re.sub('-', '_', slug))
        self.dir = dir 
        self.birt_dir = birtDir 
        self.archive_dir = archiveDir 
        try:
            os.makedirs(dir)
            os.makedirs(birtDir)
            os.makedirs(archiveDir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            else:
                print('Warning: directory already exists exception')
                pass
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Report(models.Model):
    title = models.CharField(max_length=500, unique=True)
    path = models.CharField(default=settings.REPORTS_DIR, max_length=1000)
    #path = models.FilePathField(path=settings.REPORTS_DIR, recursive=True, max_length=1000)
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    creator = models.CharField(max_length=50)
    size = models.FloatField()
    users = models.ManyToManyField(User, through='UserReport')
    # groups= models.ManyToManyField(User, through='GroupReport')
    category = models.ForeignKey(Category)
    type = models.CharField(max_length=1,
                            choices=(('P', 'Already Generated Report'), ('R', 'Real Time Manually Generated Report')),
                            default='P')
    comment = models.TextField(max_length=4000)

    def __str__(self):
        return self.title


class ReportArchive(models.Model):
    title = models.CharField(max_length=500)
    path = models.CharField(default=settings.REPORTS_DIR, max_length=1000)
    #path = models.FilePathField(path=settings.REPORTS_DIR, recursive=True, max_length=1000)
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    creator = models.CharField(max_length=50)
    size = models.FloatField()
    users = models.ManyToManyField(User, through='UserReportArch')
    category = models.ForeignKey(Category)
    type = models.CharField(max_length=1,
                            choices=(('P', 'Already Generated Report'), ('R', 'Real Time Manually Generated Report')),
                            default='P')
    comment = models.TextField(max_length=4000)

    def __str__(self):
        return self.title


class UserReport(models.Model):

    user = models.ForeignKey(User)
    report = models.ForeignKey(Report)

    def __str__(self):
        return '{} - {} '.format(self.user, self.report)

'''
class GroupReport(models.Model):

    group = models.ForeignKey(Group)
    report = models.ForeignKey(Report)

    def __str__(self):
        return '{} - {} '.format(self.group, self.report)
'''


class UserReportArch(models.Model):

    user = models.ForeignKey(User)
    report = models.ForeignKey(ReportArchive)

    def __str__(self):
        return '{} - {} '.format(self.user, self.report)


class RequestReport(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=500)
    description = models.TextField()
    attachment = models.FileField(upload_to='attachments', blank=True)
    frequency = models.CharField(max_length=1,
                            choices=(('O', 'One Time'), ('R', 'Regular')))
    url = models.URLField(max_length=500, blank=True)
    status = models.CharField(max_length=1, null=True, blank=True,
                            choices=(('A', 'Accepted'), ('R', 'Rejected'), ('I', 'In Progress'), ('D', 'Done')))
    
    def __str__(self):
        return self.title

