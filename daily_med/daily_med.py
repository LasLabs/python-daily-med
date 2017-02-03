# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import requests

from . import models

from .hl7 import str_to_time
from .request_paginator import RequestPaginator


class DailyMed(object):
    """ It provides Python bindings to the Daily Med API.

    Additional documentation regarding the API endpoints is available at
    https://dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm
    """

    API_BASE = 'https://dailymed.nlm.nih.gov/dailymed/services/v2'

    def get_spls(self, **kwargs):
        """ get_spls returns an iterator of matching SPL Meta Data.

        For more information about SPLs (Structured Product Labels), please
        visit the FDA documentation.

        Args:
            application_number (str): New Drug Application (NDA) number. See
                the documentation for resource /applicationnumbers for more
                information.
            boxed_warning (bool): Whether or not a drug contains a boxed
                warning.
            dea_schedule_code (str): Code representing a Drug Enforcement
                Administration Schedule for drugs. See the FDA documentation
                for DEA Schedules for more information. Acceptable values are
                listed below:
                    * none - Not Scheduled.
                    * C48672 - CI.
                    * C48675 - CII.
                    * C48676 - CIII.
                    * C48677 - CIV.
                    * C48679 - CV.
            doctype (str): FDA's Logical Observation Identifiers Names
                and Codes system. Determines the type of document or content
                of a label.
            drug_class_code (str): Code representing a pharmacologic drug
                class. See the documentation for resource /drugclasses
                for more information.
            drug_class_coding_system (str): Used with drug_class_code
                to specify the coding system of the drug class code.
                Acceptable values are listed below:
                    * 2.16.840.1.113883.3.26.1.5 - National Drug File
                      Reference Terminology. (Default value)
            drug_name (str): Generic or brand name. See the documentation
                for resource /drugnames for more information.
            name_type (str): Used with drug_name to specify whether the given
                name is a generic name or brand name. Acceptable values are
                listed below:
                    * `g` or `generic` - Generic name.
                    * `b` or `brand` - Brand name.
                    * `both` - Either generic or brand name. (Default value)
            labeler (str): Name of labeler for the drug.
            manufacturer (str): Name of manufacturer for the drug.
            marketing_category_code (str): FDA's Marketing Categories for
                types of drugs. See the FDA documentation for Marketing
                Category for more information.
            ndc (str): National Drug Code (NDC). See the documentation for
                resource /ndcs for more information.
            published_date (str): The date that the drug was published on
                DailyMed. The accepted date format is YYYY-MM-DD
                (ex. 2015-09-10)
            published_date_comparison (str): Used with published_date to
                specify the type of comparison used with the date. Acceptable
                values are listed below:
                    * `lt` - Drugs that have a published date Less Than
                      the published_date parameter.
                    * `lte` - Drugs that have a published date Less Than
                      or Equal To the published_date parameter.
                    * `gt` - Drugs that have a published date Greater Than
                       the published_date parameter.
                    * `gte` - Drugs that have a published date Greater Than
                       or Equal To the published_date parameter.
                    * `eq` - Drugs that have a published date Equal
                      To the published_date parameter (Default value)
            rxcui (str): RxNorm Concept Unique Identifier (RXCUI) code.
                See the documentation for resource /rxcuis for more
                information.
            setid (str): Set ID of a label.
            unii_code (str): Unique Ingredient Identifier (UNII) code.
                See the documentation for resource /uniis for more
                information.
        Returns:
            SPL: Object containing metadata, but no document.
        """
        return self.call('spls', models.SPL, kwargs)

    def get_spl(self, set_id):
        """ get_spl returns an SPLDocument for the set_id.

        Args:
            set_id (str): Set ID of the label.
        Returns:
            SPL: Object containing both the metadada and document.
        """
        response = requests.get(
            url='%s/spls/%s.xml' % (self.API_BASE, set_id),
        )
        spl_document = models.spl_document.parseString(
            response.text, silence=True,
        )
        title_vals = models.spl_document.get_all_values(
            spl_document.title.content_
        )
        return models.SPL(
            set_id=spl_document.id.root,
            title=' '.join([val for val in title_vals if val.strip()]),
            spl_version=spl_document.versionNumber.value,
            published_date=str_to_time(spl_document.effectiveTime.value),
            document=spl_document,
        )

    def call(self, endpoint, output_type, params=None):
        """ It calls the remote endpoint and returns the result, if success.

        Args:
            endpoint (str): DailyMed endpoint to call (e.g. ``ndcs``).
            output_type (type): Class type to output. Object will be
                instantiated using the current row before output.
            params: (dict|bytes) Data to be sent in the query string
                for the Request.
        Returns:
            RequestPaginator: Iterator representing all pages of the call
                result.
        Raises:
            DailyMedRemoteException: In the event of something that is TBD.
        """
        endpoint = '%s.json' % '/'.join((self.API_BASE, endpoint))
        return RequestPaginator(endpoint, params, output_type=output_type)
