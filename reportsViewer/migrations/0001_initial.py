# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('reportsViewer_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('dir', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1500)),
            ('birt_dir', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1500)),
            ('archive_dir', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1500)),
        ))
        db.send_create_signal('reportsViewer', ['Category'])

        # Adding model 'Report'
        db.create_table('reportsViewer_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500)),
            ('path', self.gf('django.db.models.fields.CharField')(default='/home/users/mhristov/ibcs/data/reportsViewer', max_length=1000)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('size', self.gf('django.db.models.fields.FloatField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reportsViewer.Category'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=4000)),
        ))
        db.send_create_signal('reportsViewer', ['Report'])

        # Adding model 'ReportArchive'
        db.create_table('reportsViewer_reportarchive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('path', self.gf('django.db.models.fields.CharField')(default='/home/users/mhristov/ibcs/data/reportsViewer', max_length=1000)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('size', self.gf('django.db.models.fields.FloatField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reportsViewer.Category'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=4000)),
        ))
        db.send_create_signal('reportsViewer', ['ReportArchive'])

        # Adding model 'UserReport'
        db.create_table('reportsViewer_userreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reportsViewer.Report'])),
        ))
        db.send_create_signal('reportsViewer', ['UserReport'])

        # Adding model 'UserReportArch'
        db.create_table('reportsViewer_userreportarch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reportsViewer.ReportArchive'])),
        ))
        db.send_create_signal('reportsViewer', ['UserReportArch'])

        # Adding model 'RequestReport'
        db.create_table('reportsViewer_requestreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True, null=True)),
        ))
        db.send_create_signal('reportsViewer', ['RequestReport'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('reportsViewer_category')

        # Deleting model 'Report'
        db.delete_table('reportsViewer_report')

        # Deleting model 'ReportArchive'
        db.delete_table('reportsViewer_reportarchive')

        # Deleting model 'UserReport'
        db.delete_table('reportsViewer_userreport')

        # Deleting model 'UserReportArch'
        db.delete_table('reportsViewer_userreportarch')

        # Deleting model 'RequestReport'
        db.delete_table('reportsViewer_requestreport')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'reportsViewer.category': {
            'Meta': {'object_name': 'Category'},
            'archive_dir': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1500'}),
            'birt_dir': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1500'}),
            'dir': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'reportsViewer.report': {
            'Meta': {'object_name': 'Report'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reportsViewer.Category']"}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "'/home/users/mhristov/ibcs/data/reportsViewer'", 'max_length': '1000'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'size': ('django.db.models.fields.FloatField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'through': "orm['reportsViewer.UserReport']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'reportsViewer.reportarchive': {
            'Meta': {'object_name': 'ReportArchive'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reportsViewer.Category']"}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "'/home/users/mhristov/ibcs/data/reportsViewer'", 'max_length': '1000'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'size': ('django.db.models.fields.FloatField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'through': "orm['reportsViewer.UserReportArch']"}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'reportsViewer.requestreport': {
            'Meta': {'object_name': 'RequestReport'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'reportsViewer.userreport': {
            'Meta': {'object_name': 'UserReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reportsViewer.Report']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'reportsViewer.userreportarch': {
            'Meta': {'object_name': 'UserReportArch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reportsViewer.ReportArchive']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['reportsViewer']