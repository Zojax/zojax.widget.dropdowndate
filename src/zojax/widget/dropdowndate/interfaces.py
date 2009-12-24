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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from z3c.form.interfaces import IWidget

_ = MessageFactory('zojax.widget.dropdowndate')


class IMonthDropdownDate(schema.interfaces.IDate):
    """ month date field """


class IDropdownDate(schema.interfaces.IDate):
    """ date field """


class IDropdownDatetime(schema.interfaces.IDatetime):
    """ datetime field """


class IDateDropdownWidget(IWidget):
    """ date widget """


class IDatetimeDropdownWidget(IWidget):
    """ datetime widget """


class IMonthDropdownWidget(IWidget):
    """ month widget """
