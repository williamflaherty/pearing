# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Conversation'
        db.delete_table(u'dateme_app_conversation')

        # Deleting field 'Message.conversation'
        db.delete_column(u'dateme_app_message', 'conversation_id')

        # Adding field 'Message.receiver'
        db.add_column(u'dateme_app_message', 'receiver',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='receiver', to=orm['auth.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Conversation'
        db.create_table(u'dateme_app_conversation', (
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dateme_app', ['Conversation'])

        # Adding field 'Message.conversation'
        db.add_column(u'dateme_app_message', 'conversation',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['dateme_app.Conversation']),
                      keep_default=False)

        # Deleting field 'Message.receiver'
        db.delete_column(u'dateme_app_message', 'receiver_id')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dateme_app.contenttype': {
            'Meta': {'object_name': 'ContentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dateme_app.message': {
            'Meta': {'object_name': 'Message'},
            'contentType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': u"orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'to': u"orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'dateme_app.person': {
            'Meta': {'object_name': 'Person'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isValidated': ('django.db.models.fields.BooleanField', [], {}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'dateme_app.setting': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('user', 'name'),)", 'object_name': 'Setting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['dateme_app']