# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from .spl_document import POCP_MT050100UV_Document


class SPL(properties.HasProperties):
    """ SPL provides Structured Product Label meta + document. """

    set_id = properties.String(
        'Set ID',
    )
    title = properties.String(
        'Title',
    )
    spl_version = properties.String(
        'Version',
    )
    published_date = properties.DateTime(
        'Published Date',
    )
    document = properties.Instance(
        'Structured Product Label Document',
        POCP_MT050100UV_Document,
        required=False,
    )
