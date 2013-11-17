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

        # Adding model 'Challenge'
        db.create_table(u'dateme_app_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dateme_app', ['Challenge'])

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

        # Deleting field 'Person.isValidated'
        db.delete_column(u'dateme_app_person', 'isValidated')

        # Deleting field 'Person.user'
        db.delete_column(u'dateme_app_person', 'user_id')

        # Adding field 'Person.username'
        db.add_column(u'dateme_app_person', 'username',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=100),
                      keep_default=False)

        # Adding field 'Person.handle'
        db.add_column(u'dateme_app_person', 'handle',
                      self.gf('django.db.models.fields.CharField')(default=1, unique=True, max_length=35),
                      keep_default=False)

        # Adding field 'Person.token'
        db.add_column(u'dateme_app_person', 'token',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=200),
                      keep_default=False)

        # Adding field 'Person.birthday'
        db.add_column(u'dateme_app_person', 'birthday',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 17, 0, 0)),
                      keep_default=False)

        # Adding field 'Person.age_start'
        db.add_column(u'dateme_app_person', 'age_start',
                      self.gf('django.db.models.fields.IntegerField')(default=18),
                      keep_default=False)

        # Adding field 'Person.age_end'
        db.add_column(u'dateme_app_person', 'age_end',
                      self.gf('django.db.models.fields.IntegerField')(default=22),
                      keep_default=False)

        # Adding field 'Person.gender'
        db.add_column(u'dateme_app_person', 'gender',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='gender', to=orm['dateme_app.Gender']),
                      keep_default=False)

        # Adding M2M table for field orientation on 'Person'
        m2m_table_name = db.shorten_name(u'dateme_app_person_orientation')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'dateme_app.person'], null=False)),
            ('gender', models.ForeignKey(orm[u'dateme_app.gender'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'gender_id'])

        # Deleting field 'Message.receiver'
        db.delete_column(u'dateme_app_message', 'receiver_id')

        # Adding field 'Message.conversation'
        db.add_column(u'dateme_app_message', 'conversation',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['dateme_app.Conversation']),
                      keep_default=False)


        # Changing field 'Message.sender'
        db.alter_column(u'dateme_app_message', 'sender_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Person']))

        # Changing field 'Setting.user'
        db.alter_column(u'dateme_app_setting', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Person']))

    def backwards(self, orm):
        # Deleting model 'Gender'
        db.delete_table(u'dateme_app_gender')

        # Deleting model 'Challenge'
        db.delete_table(u'dateme_app_challenge')

        # Deleting model 'Conversation'
        db.delete_table(u'dateme_app_conversation')

        # Removing M2M table for field people on 'Conversation'
        db.delete_table(db.shorten_name(u'dateme_app_conversation_people'))

        # Adding field 'Person.isValidated'
        db.add_column(u'dateme_app_person', 'isValidated',
                      self.gf('django.db.models.fields.BooleanField')(default=1),
                      keep_default=False)

        # Adding field 'Person.user'
        db.add_column(u'dateme_app_person', 'user',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['auth.User'], unique=True),
                      keep_default=False)

        # Deleting field 'Person.username'
        db.delete_column(u'dateme_app_person', 'username')

        # Deleting field 'Person.handle'
        db.delete_column(u'dateme_app_person', 'handle')

        # Deleting field 'Person.token'
        db.delete_column(u'dateme_app_person', 'token')

        # Deleting field 'Person.birthday'
        db.delete_column(u'dateme_app_person', 'birthday')

        # Deleting field 'Person.age_start'
        db.delete_column(u'dateme_app_person', 'age_start')

        # Deleting field 'Person.age_end'
        db.delete_column(u'dateme_app_person', 'age_end')

        # Deleting field 'Person.gender'
        db.delete_column(u'dateme_app_person', 'gender_id')

        # Removing M2M table for field orientation on 'Person'
        db.delete_table(db.shorten_name(u'dateme_app_person_orientation'))

        # Adding field 'Message.receiver'
        db.add_column(u'dateme_app_message', 'receiver',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='receiver', to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Message.conversation'
        db.delete_column(u'dateme_app_message', 'conversation_id')


        # Changing field 'Message.sender'
        db.alter_column(u'dateme_app_message', 'sender_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Setting.user'
        db.alter_column(u'dateme_app_setting', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

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
        u'dateme_app.message': {
            'Meta': {'object_name': 'Message'},
            'contentType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.ContentType']"}),
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Conversation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'dateme_app.person': {
            'Meta': {'object_name': 'Person'},
            'age_end': ('django.db.models.fields.IntegerField', [], {}),
            'age_start': ('django.db.models.fields.IntegerField', [], {}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gender'", 'to': u"orm['dateme_app.Gender']"}),
            'handle': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orientation': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'orientation'", 'symmetrical': 'False', 'to': u"orm['dateme_app.Gender']"}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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