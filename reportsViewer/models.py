from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Report(models.Model):
    title = models.CharField(max_length=200)
    path = models.CharField(max_length=1000)
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    users = models.ManyToManyField(User, through='UserReport')
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.title

class UserReport(models.Model):

    user = models.ForeignKey(User)
    report = models.ForeignKey(Report)

    def __str__(self):
        return '{} - {} '.format(self.user,self.report)
