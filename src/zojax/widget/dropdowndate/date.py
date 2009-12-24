##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import time
from datetime import date, datetime

from zope import interface, component, schema
from zope.datetime import parseDatetimetz
import zope.i18n
from zope.cachedescriptors.property import Lazy

from z3c.form import interfaces
from z3c.form.widget import FieldWidget, Widget
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.converter import FormatterValidationError

from interfaces import \
    IMonthDropdownWidget, IDateDropdownWidget, \
    IDatetimeDropdownWidget, IMonthDropdownDate, IDropdownDate, \
    IDropdownDatetime, _

PLACEHOLDER = object()


class BaseWidget(TextWidget):

    second   = [(str(i).zfill(2),str(i).zfill(2))  for i in range(60)]

    hour   = [(str(i).zfill(2),str(i).zfill(2))  for i in range(24)]

    day   = [(str(i+1).zfill(2),str(i+1).zfill(2))  for i in range(31)]

    type_ = datetime

    allowedSelects = ['second', 'minute', 'hour', 'day', 'month', 'year']

    allowedAttributes = ['second', 'minute', 'hour', 'day', 'month', 'year']

    type = 'dateTime'
    length = 'full'

    @Lazy
    def month(self):
        calendar = self.request.locale.dates.calendars['gregorian']
        monthNames = calendar.getMonthNames()
        return [(str(i+1).zfill(2), unicode(monthNames[i])) for i in range(12)]

    year  = [(str(i+ 1900), str(i+1900)) for i in range(130)]

    @Lazy
    def elements(self):
        return [[self.day,'day', _(u'Day')],
                [self.month,'month', _(u'Month')],
                [self.year,'year', _(u'Year')],
                [self.hour,'hour', _(u'Hour')],
                [self.second,'minute', _(u'Minute')],
                [self.second,'second', _(u'Second')]
                ]

    def update(self):
        self.locale = self.request.locale
        self.formatter = self.locale.dates.getFormatter(self.type, self.length)
        super(BaseWidget, self).update()
        data = self.value
        prefix = self.name + '.'
        idprefix = self.id + '-'
        classprefix = self.klass + '-'
        self.selects = [{'name': prefix+select[1],
                     'id': idprefix+select[1],
                     'klass': classprefix+select[1],
                     'title': select[2],
                     'hidden':  select[1] not in self.allowedSelects,
                     'value': getattr(data, select[1], interfaces.NOVALUE),
                     'items': self.renderItemsWithValues(
                         select[0], idprefix+select[1],
                         getattr(data, select[1], interfaces.NOVALUE))}
                     for select in self.elements
                     if select[1] in self.allowedAttributes
                     ]

    def renderItemsWithValues(self, values, id, selected=None):
        """ Render all values from a dropdown """
        res = []
        for i, value in enumerate(values):
            res.append(
                dict(value=value[0],
                     contents=value[1],
                     id='%s-%s'%(id, i),
                     selected=selected==int(value[0]) and 'selected' or ''))
        return res

    def extract(self, default=interfaces.NOVALUE):
        prefix = self.name + '.'
        dt = {}
        for i in self.elements:
            if i[1] not in self.allowedAttributes:
                continue
            value = self.request.form.get(prefix+i[1], PLACEHOLDER)
            if value is not PLACEHOLDER:
                try:
                    dt[i[1]] = int(value[0])
                except (TypeError, IndexError), e:
                    pass
        if not dt:
            dt = self.request.form.get(self.name, PLACEHOLDER)
            if dt is not PLACEHOLDER:
                try:
                    res = self.formatter.parse(dt)
                except zope.i18n.format.DateTimeParseError, err:
                    res = parseDatetimetz(dt)
                return self.type_(res.year, res.month, res.day)
        else:
            return self.formatter.parse(self.formatter.format(self.type_(**dt)))
        return default


class DatetimeWidget(BaseWidget):
    interface.implements(IDatetimeDropdownWidget)

    klass = 'widget-dropdown-datetime'


class DateWidget(BaseWidget):
    interface.implements(IDateDropdownWidget)

    klass = 'widget-dropdown-date'
    type = 'date'
    type_ = date

    allowedSelects = ['day', 'month', 'year']

    allowedAttributes = ['day', 'month', 'year']


class MonthWidget(BaseWidget):
    interface.implements(IMonthDropdownWidget)

    klass = 'widget-dropdown-month'
    type = 'date'
    type_ = date

    allowedSelects = ['month', 'year']

    allowedAttributes = ['day', 'month', 'year']


@component.adapter(IMonthDropdownDate, interfaces.IFormLayer)
@interface.implementer(interfaces.IFieldWidget)
def MonthFieldWidget(field, request):
    """IFieldWidget factory for MonthWidget."""
    return FieldWidget(field, MonthWidget(request))


@component.adapter(IDropdownDate, interfaces.IFormLayer)
@interface.implementer(interfaces.IFieldWidget)
def DateFieldWidget(field, request):
    """IFieldWidget factory for DateWidget."""
    return FieldWidget(field, DateWidget(request))


@component.adapter(IDropdownDatetime, interfaces.IFormLayer)
@interface.implementer(interfaces.IFieldWidget)
def DatetimeFieldWidget(field, request):
    """IFieldWidget factory for DatetimeWidget."""
    return FieldWidget(field, DatetimeWidget(request))


class MonthDataConverter(BaseDataConverter):
    component.adapts(schema.interfaces.IDate, IMonthDropdownWidget)

    type = 'date'
    length = 'short'

    def toWidgetValue(self, value):
        return date(value.year, value.month, 1)

    def toFieldValue(self, value):
        return value


class DateDataConverter(BaseDataConverter):
    component.adapts(schema.interfaces.IDate, IDateDropdownWidget)

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        return value


class DatetimeDataConverter(BaseDataConverter):
    component.adapts(schema.interfaces.IDatetime, IDatetimeDropdownWidget)

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        return value
