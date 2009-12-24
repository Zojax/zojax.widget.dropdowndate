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
from zope import schema, interface
from zojax.content.type.item import PersistentItem

from zojax.widget.dropdowndate.field import MonthDropdownDate, DropdownDate, DropdownDatetime



class IPage1(interface.Interface):

    title = schema.TextLine(
        title = u'Title',
        description = u'Page title.',
        required = True)

    description = schema.Text(
        title = u'Description',
        description = u'A short summary of the content.',
        required = False)

    date = MonthDropdownDate(
        title = u'Month',
        required = True)


class Page1(PersistentItem):
    interface.implements(IPage1)


class IPage2(interface.Interface):

    title = schema.TextLine(
        title = u'Title',
        description = u'Page title.',
        required = True)

    description = schema.Text(
        title = u'Description',
        description = u'A short summary of the content.',
        required = False)

    date = DropdownDate(
        title = u'Date',
        required = True)


class Page2(PersistentItem):
    interface.implements(IPage2)

class IPage3(interface.Interface):

    title = schema.TextLine(
        title = u'Title',
        description = u'Page title.',
        required = True)

    description = schema.Text(
        title = u'Description',
        description = u'A short summary of the content.',
        required = False)

    date = DropdownDatetime(
        title = u'Date',
        required = True)


class Page3(PersistentItem):
    interface.implements(IPage3)
