# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        db.execute('CREATE EXTENSION IF NOT EXISTS hstore;')

        # Adding model 'LoggedAction'
        db.create_table(u'pgaudit_loggedaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table_name', self.gf('django.db.models.fields.TextField')()),
            ('oid', self.gf('django.db.models.fields.IntegerField')()),
            ('session_user_name', self.gf('django.db.models.fields.TextField')()),
            ('action_tstamp_tx', self.gf('django.db.models.fields.DateTimeField')()),
            ('action_tstamp_stm', self.gf('django.db.models.fields.DateTimeField')()),
            ('action_tstamp_clk', self.gf('django.db.models.fields.DateTimeField')()),
            ('transaction_id', self.gf('django.db.models.fields.IntegerField')()),
            ('application_name', self.gf('django.db.models.fields.TextField')()),
            ('client_addr', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('client_port', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('client_query', self.gf('django.db.models.fields.TextField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('row_data', self.gf('djorm_hstore.fields.DictionaryField')(db_index=True)),
            ('changed_fields', self.gf('djorm_hstore.fields.DictionaryField')(null=True, blank=True)),
            ('statement_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pgaudit', ['LoggedAction'])


    def backwards(self, orm):
        # Deleting model 'LoggedAction'
        db.delete_table(u'pgaudit_loggedaction')


    models = {
        u'pgaudit.loggedaction': {
            'Meta': {'object_name': 'LoggedAction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_tstamp_clk': ('django.db.models.fields.DateTimeField', [], {}),
            'action_tstamp_stm': ('django.db.models.fields.DateTimeField', [], {}),
            'action_tstamp_tx': ('django.db.models.fields.DateTimeField', [], {}),
            'application_name': ('django.db.models.fields.TextField', [], {}),
            'changed_fields': ('djorm_hstore.fields.DictionaryField', [], {}),
            'client_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'client_port': ('django.db.models.fields.IntegerField', [], {}),
            'client_query': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oid': ('django.db.models.fields.IntegerField', [], {}),
            'row_data': ('djorm_hstore.fields.DictionaryField', [], {}),
            'session_user_name': ('django.db.models.fields.TextField', [], {}),
            'statement_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'table_name': ('django.db.models.fields.TextField', [], {}),
            'transaction_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['pgaudit']
