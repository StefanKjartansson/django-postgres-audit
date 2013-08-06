# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


audit_table = '''
CREATE OR REPLACE FUNCTION audit_table(target_table regclass, audit_rows boolean, audit_query_text boolean, ignored_cols text[]) RETURNS void AS $body$
DECLARE
  stm_targets text = 'INSERT OR UPDATE OR DELETE OR TRUNCATE';
  _q_txt text;
  _ignored_cols_snip text = '';
BEGIN
    EXECUTE 'DROP TRIGGER IF EXISTS audit_trigger_row ON ' || quote_ident(target_table::text);
    EXECUTE 'DROP TRIGGER IF EXISTS audit_trigger_stm ON ' || quote_ident(target_table::text);

    IF audit_rows THEN
        IF array_length(ignored_cols,1) > 0 THEN
            _ignored_cols_snip = ', ' || quote_literal(ignored_cols);
        END IF;
        _q_txt = 'CREATE TRIGGER audit_trigger_row AFTER INSERT OR UPDATE OR DELETE ON ' ||
                 quote_ident(target_table::text) ||
                 ' FOR EACH ROW EXECUTE PROCEDURE if_modified_func(' ||
                 quote_literal(audit_query_text) || _ignored_cols_snip || ');';
        RAISE NOTICE '%%',_q_txt;
        EXECUTE _q_txt;
        stm_targets = 'TRUNCATE';
    ELSE
    END IF;

    _q_txt = 'CREATE TRIGGER audit_trigger_stm AFTER ' || stm_targets || ' ON ' ||
             quote_ident(target_table::text) ||
             ' FOR EACH STATEMENT EXECUTE PROCEDURE if_modified_func('||
             quote_literal(audit_query_text) || ');';
    RAISE NOTICE '%%',_q_txt;
    EXECUTE _q_txt;

END;
$body$
language 'plpgsql';

CREATE OR REPLACE FUNCTION audit_table(target_table regclass, audit_rows boolean, audit_query_text boolean) RETURNS void AS $body$
SELECT audit_table($1, $2, $3, ARRAY[]::text[]);
$body$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION audit_table(target_table regclass) RETURNS void AS $$
SELECT audit_table($1, BOOLEAN 't', BOOLEAN 't');
$$ LANGUAGE 'sql';
'''


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute(audit_table)

    def backwards(self, orm):
        db.execute('DROP FUNCTION IF EXISTS audit_table;')

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
