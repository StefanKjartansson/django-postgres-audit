#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals, print_function, absolute_import

from django.db import models

from pgaudit.mixins import AuditMixin


class SimpleTable(models.Model, AuditMixin):

    name = models.CharField(max_length=16)
