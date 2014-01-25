# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Gender'
        db.create_table(u'dateme_app_gender', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'dateme_app', ['Gender'])

        # Adding model 'Person'
        db.create_table(u'dateme_app_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')()),
            ('age_start', self.gf('django.db.models.fields.IntegerField')()),
            ('age_end', self.gf('django.db.models.fields.IntegerField')()),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gender', to=orm['dateme_app.Gender'])),
        ))
        db.send_create_signal(u'dateme_app', ['Person'])

        # Adding M2M table for field orientation on 'Person'
        m2m_table_name = db.shorten_name(u'dateme_app_person_orientation')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'dateme_app.person'], null=False)),
            ('gender', models.ForeignKey(orm[u'dateme_app.gender'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'gender_id'])

        # Adding model 'Setting'
        db.create_table(u'dateme_app_setting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Person'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'dateme_app', ['Setting'])

        # Adding unique constraint on 'Setting', fields ['user', 'name']
        db.create_unique(u'dateme_app_setting', ['user_id', 'name'])

        # Adding model 'ContentType'
        db.create_table(u'dateme_app_contenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'dateme_app', ['ContentType'])

        # Adding model 'Conversation'
        db.create_table(u'dateme_app_conversation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dateme_app', ['Conversation'])

        # Adding M2M table for field people on 'Conversation'
        m2m_table_name = db.shorten_name(u'dateme_app_conversation_people')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conversation', models.ForeignKey(orm[u'dateme_app.conversation'], null=False)),
            ('person', models.ForeignKey(orm[u'dateme_app.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conversation_id', 'person_id'])

        # Adding model 'Message'
        db.create_table(u'dateme_app_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contentType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.ContentType'])),
            ('conversation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Conversation'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Person'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'dateme_app', ['Message'])

        # Adding model 'Challenge'
        db.create_table(u'dateme_app_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dateme_app', ['Challenge'])

        # Adding model 'Location'
        db.create_table(u'dateme_app_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Person'])),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'dateme_app', ['Location'])

        # Adding model 'MessageChallenge'
        db.create_table(u'dateme_app_messagechallenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Challenge'])),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Message'])),
            ('picture', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Person'])),
            ('isComplete', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'dateme_app', ['MessageChallenge'])

        # Adding model 'PhotoLink'
        db.create_table(u'dateme_app_photolink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Person'])),
        ))
        db.send_create_signal(u'dateme_app', ['PhotoLink'])


    def backwards(self, orm):
        # Removing unique constraint on 'Setting', fields ['user', 'name']
        db.delete_unique(u'dateme_app_setting', ['user_id', 'name'])

        # Deleting model 'Gender'
        db.delete_table(u'dateme_app_gender')

        # Deleting model 'Person'
        db.delete_table(u'dateme_app_person')

        # Removing M2M table for field orientation on 'Person'
        db.delete_table(db.shorten_name(u'dateme_app_person_orientation'))

        # Deleting model 'Setting'
        db.delete_table(u'dateme_app_setting')

        # Deleting model 'ContentType'
        db.delete_table(u'dateme_app_contenttype')

        # Deleting model 'Conversation'
        db.delete_table(u'dateme_app_conversation')

        # Removing M2M table for field people on 'Conversation'
        db.delete_table(db.shorten_name(u'dateme_app_conversation_people'))

        # Deleting model 'Message'
        db.delete_table(u'dateme_app_message')

        # Deleting model 'Challenge'
        db.delete_table(u'dateme_app_challenge')

        # Deleting model 'Location'
        db.delete_table(u'dateme_app_location')

        # Deleting model 'MessageChallenge'
        db.delete_table(u'dateme_app_messagechallenge')

        # Deleting model 'PhotoLink'
        db.delete_table(u'dateme_app_photolink')


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
            'age_end': ('django.db.models.fields.IntegerField', [], {}),
            'age_start': ('django.db.models.fields.IntegerField', [], {}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gender'", 'to': u"orm['dateme_app.Gender']"}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orientation': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'orientation'", 'symmetrical': 'False', 'to': u"orm['dateme_app.Gender']"}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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