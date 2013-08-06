#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals, print_function, absolute_import

from django.db import connection

from djorm_hstore.expressions import HstoreExpression as HE

from .models import LoggedAction


def audit_table(model):
    q = "SELECT audit_table('%s');" % model._meta.db_table
    cursor = connection.cursor()
    cursor.execute(q)


class AuditMixin:

    def audit_history(self):

        return LoggedAction.objects \
            .filter(table_name=self._meta.db_table) \
            .where(HE("row_data").contains({'id': str(self.id)}))
