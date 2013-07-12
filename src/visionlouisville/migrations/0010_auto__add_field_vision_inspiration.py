# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Vision.inspiration'
        db.add_column(u'visionlouisville_vision', 'inspiration',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['visionlouisville.Moment'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Vision.inspiration'
        db.delete_column(u'visionlouisville_vision', 'inspiration_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'visionlouisville.moment': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'Moment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'visionlouisville.reply': {
            'Meta': {'object_name': 'Reply'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'vision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': u"orm['visionlouisville.Vision']"})
        },
        u'visionlouisville.share': {
            'Meta': {'object_name': 'Share'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shares'", 'to': u"orm['auth.User']"}),
            'vision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['visionlouisville.Vision']"})
        },
        u'visionlouisville.vision': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'Vision'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visions'", 'to': u"orm['auth.User']"}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspiration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['visionlouisville.Moment']", 'null': 'True', 'blank': 'True'}),
            'sharers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sharers'", 'symmetrical': 'False', 'through': u"orm['visionlouisville.Share']", 'to': u"orm['auth.User']"}),
            'supporters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'supported'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['visionlouisville']