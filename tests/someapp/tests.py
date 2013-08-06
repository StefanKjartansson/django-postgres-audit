#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals, print_function, absolute_import

from django.test import TestCase
from pgaudit.mixins import audit_table

from .models import SimpleTable


class TestSimpleTableTrigger(TestCase):
    def test_simple(self):
        """
        """
        audit_table(SimpleTable)
        s = SimpleTable(name="foobar")
        s.save()
        s.name = "moobar"
        s.save()
        self.assertEqual(s.audit_history().count(), 2)
