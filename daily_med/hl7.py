# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

""" hl7.py Provides tools related to coercing HL7 formats. """

from datetime import datetime

FMT_DATE = '%Y%m%d'
FMT_TIME = '%H:%M'
FMT_DATETIME = '%s%s' % (FMT_DATE, FMT_TIME)


def str_to_time(date_str):
    """ str_to_time returns a date(time) object representing date_str.

    Returns:
        datetime: Object representing date string.
    """
    if 'T' in date_str:
        return datetime.strptime(date_str, FMT_DATETIME)
    return datetime.strptime(date_str, FMT_DATE)
