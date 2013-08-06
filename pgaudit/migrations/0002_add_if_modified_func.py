# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


if_modified_func = """
CREATE OR REPLACE FUNCTION if_modified_func() RETURNS TRIGGER AS $body$
DECLARE
    row pgaudit_loggedaction;
    include_values boolean;
    log_diffs boolean;
    h_old hstore;
    h_new hstore;
    excluded_cols text[] = ARRAY[]::text[];
BEGIN
    IF TG_WHEN <> 'AFTER' THEN
        RAISE EXCEPTION 'if_modified_func() may only run as an AFTER trigger';
    END IF;

    row = ROW(
        nextval('pgaudit_loggedaction_id_seq'), -- event_id
        TG_TABLE_NAME::text,                          -- table_name
        TG_RELID::int,                                -- relation OID for much quicker searches
        session_user::text,                           -- session_user_name
        current_timestamp,                            -- action_tstamp_tx
        statement_timestamp(),                        -- action_tstamp_stm
        clock_timestamp(),                            -- action_tstamp_clk
        txid_current(),                               -- transaction ID
        (SELECT setting FROM pg_settings WHERE name = 'application_name'),
        inet_client_addr()::text,                     -- client_addr
        inet_client_port(),                           -- client_port
        current_query(),                              -- top-level query or queries (if multistatement) from client
        substring(TG_OP,1,1),                         -- action
        NULL, NULL,                                   -- row_data, changed_fields
        'f'                                           -- statement_only
        );

    IF NOT TG_ARGV[0]::boolean IS DISTINCT FROM 'f'::boolean THEN
        row.client_query = NULL;
    END IF;

    IF TG_ARGV[1] IS NOT NULL THEN
        excluded_cols = TG_ARGV[1]::text[];
    END IF;

    IF (TG_OP = 'UPDATE' AND TG_LEVEL = 'ROW') THEN
        row.row_data = hstore(OLD.*);
        row.changed_fields =  (hstore(NEW.*) - row.row_data) - excluded_cols;
        IF row.changed_fields = hstore('') THEN
            -- All changed fields are ignored. Skip this update.
            RETURN NULL;
        END IF;
    ELSIF (TG_OP = 'DELETE' AND TG_LEVEL = 'ROW') THEN
        row.row_data = hstore(OLD.*) - excluded_cols;
    ELSIF (TG_OP = 'INSERT' AND TG_LEVEL = 'ROW') THEN
        row.row_data = hstore(NEW.*) - excluded_cols;
    ELSIF (TG_LEVEL = 'STATEMENT' AND TG_OP IN ('INSERT','UPDATE','DELETE','TRUNCATE')) THEN
        row.statement_only = 't';
    ELSE
        RAISE EXCEPTION '[if_modified_func] - Trigger func added as trigger for unhandled case: %%, %%',TG_OP, TG_LEVEL;
        RETURN NULL;
    END IF;

    INSERT INTO pgaudit_loggedaction VALUES (row.*);
    RETURN NULL;
END;
$body$
LANGUAGE plpgsql;
"""


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute(if_modified_func)

    def backwards(self, orm):
        db.execute('DROP FUNCTION IF EXISTS if_modified_func;')

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
