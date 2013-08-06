#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals, print_function, absolute_import

from django.db import models

from djorm_hstore.fields import DictionaryField
from djorm_hstore.models import HStoreManager


class LoggedAction(models.Model):
    table_name = models.TextField()
    oid = models.IntegerField()
    session_user_name = models.TextField()
    action_tstamp_tx = models.DateTimeField()
    action_tstamp_stm = models.DateTimeField()
    action_tstamp_clk = models.DateTimeField()
    transaction_id = models.IntegerField()
    application_name = models.TextField()
    client_addr = models.IPAddressField(null=True, blank=True)
    client_port = models.IntegerField(null=True, blank=True)
    client_query = models.TextField()
    action = models.CharField(max_length=1)
    row_data = DictionaryField(db_index=True)
    changed_fields = DictionaryField(null=True, blank=True)
    statement_only = models.BooleanField()

    objects = HStoreManager()
