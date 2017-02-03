# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import os
import unittest

from properties import HasProperties as BaseModel

from ..daily_med import DailyMed
from ..models import SPL


mock_path = 'daily_med.daily_med'


class TestDailyMed(unittest.TestCase):

    def setUp(self):
        self.dm = DailyMed()

    def get_sample_xml(self):
        xml_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'spl_doc_1.xml',
        )
        with open(xml_path, 'r') as fh:
            return fh.read()

    @mock.patch('%s.RequestPaginator' % mock_path)
    def test_call(self, paginator):
        """ It should create a RequestPaginator w/ the proper args. """
        self.dm.API_BASE = 'base'
        params = {'params': 1}
        self.dm.call('endpoint', BaseModel, params)
        paginator.assert_called_once_with(
            'base/endpoint.json', params, output_type=BaseModel,
        )

    @mock.patch('%s.RequestPaginator' % mock_path)
    def test_call_return(self, paginator):
        """ It should return the paginator. """
        res = self.dm.call('endpoint', BaseModel)
        self.assertEqual(res, paginator())

    @mock.patch('%s.requests' % mock_path)
    def test_get_spl_request(self, requests):
        """ It should request the proper URI. """
        text_mock = mock.MagicMock()
        text_mock.text = self.get_sample_xml()
        requests.get.return_value = text_mock
        self.dm.API_BASE = 'base'
        self.dm.get_spl('set_id')
        requests.get.assert_called_once_with(
            url='base/spls/set_id.xml',
        )

    @mock.patch('%s.requests' % mock_path)
    def test_get_spl_return(self, requests):
        """ It should return an SPLDocument """
        text_mock = mock.MagicMock()
        text_mock.text = self.get_sample_xml()
        requests.get.return_value = text_mock
        res = self.dm.get_spl('set_id')
        self.assertIsInstance(res, SPL)

    def test_get_spls(self):
        """ It should make the proper call and return it. """
        with mock.patch.object(self.dm, 'call') as call:
            kwargs = {'kwargs': 'sZdsdfd'}
            res = self.dm.get_spls(**kwargs)
            call.assert_called_once_with(
                'spls', SPL, kwargs,
            )
            self.assertEqual(res, call())
