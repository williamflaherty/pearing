# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.orientation'
        db.add_column(u'dateme_app_person', 'orientation',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='orientation', to=orm['dateme_app.Gender']),
                      keep_default=False)

        # Removing M2M table for field orientation on 'Person'
        db.delete_table(db.shorten_name(u'dateme_app_person_orientation'))


        # Changing field 'Person.birthday'
        db.alter_column(u'dateme_app_person', 'birthday', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):
        # Deleting field 'Person.orientation'
        db.delete_column(u'dateme_app_person', 'orientation_id')

        # Adding M2M table for field orientation on 'Person'
        m2m_table_name = db.shorten_name(u'dateme_app_person_orientation')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'dateme_app.person'], null=False)),
            ('gender', models.ForeignKey(orm[u'dateme_app.gender'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'gender_id'])


        # Changing field 'Person.birthday'
        db.alter_column(u'dateme_app_person', 'birthday', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'dateme_app.challenge': {
            'Meta': {'object_name': 'Challenge'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dateme_app.contenttype': {
            'Meta': {'object_name': 'ContentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dateme_app.conversation': {
            'Meta': {'object_name': 'Conversation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dateme_app.Person']", 'symmetrical': 'False'})
        },
        u'dateme_app.gender': {
            'Meta': {'object_name': 'Gender'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'dateme_app.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"})
        },
        u'dateme_app.message': {
            'Meta': {'object_name': 'Message'},
            'contentType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.ContentType']"}),
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Conversation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'dateme_app.messagechallenge': {
            'Meta': {'object_name': 'MessageChallenge'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isComplete': ('django.db.models.fields.BooleanField', [], {}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Message']"}),
            'picture': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"})
        },
        u'dateme_app.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'age_end': ('django.db.models.fields.IntegerField', [], {}),
            'age_start': ('django.db.models.fields.IntegerField', [], {}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gender'", 'to': u"orm['dateme_app.Gender']"}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orientation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orientation'", 'to': u"orm['dateme_app.Gender']"}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'token_expiration': ('django.db.models.fields.DateTimeField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dateme_app.photolink': {
            'Meta': {'object_name': 'PhotoLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"})
        },
        u'dateme_app.setting': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('user', 'name'),)", 'object_name': 'Setting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['dateme_app']