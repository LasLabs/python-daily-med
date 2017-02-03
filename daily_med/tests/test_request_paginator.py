# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest

from ..request_paginator import RequestPaginator


class TestRequestPaginator(unittest.TestCase):

    def setUp(self):
        self.vals = {
            'endpoint': 'endpoint',
            'params': {'param': 1},
            'page_size': 30,
            'page_start': 3,
            'output_type': dict,
        }
        self.test_responses = [
            {
                'metadata': {
                    'current_page': 1,
                    'total_pages': 3,
                },
                'data': [{
                    'page': 1,
                }],
            },
            {
                'metadata': {
                    'current_page': 2,
                    'total_pages': 3,
                },
                'data': [{
                    'page': 2,
                }],
            },
            {
                'metadata': {
                    'current_page': 3,
                    'total_pages': 3,
                },
                'data': [{
                    'page': 3,
                }],
            },
        ]
        self.paginator = RequestPaginator(**self.vals)

    def test_init_attrs(self):
        """ It should correctly assign instance attributes. """
        attrs = {
            attr: getattr(self.paginator, attr) for attr in self.vals.keys()
        }
        self.assertDictEqual(attrs, self.vals)

    @mock.patch('daily_med.request_paginator.requests')
    def test_init_session(self, requests):
        """ It should initialize a requests session. """
        paginator = RequestPaginator(**self.vals)
        self.assertEqual(paginator.session, requests.Session())

    def test_call_gets(self):
        """ It should call the session with proper args. """
        params = {'param_test': 23234}
        with mock.patch.object(self.paginator, 'session') as session:
            self.paginator.call(params)
            session.get.assert_called_once_with(
                url=self.vals['endpoint'],
                params=params,
                verify=True,
            )

    def test_call_return(self):
        """ It should return the json decoded response. """
        with mock.patch.object(self.paginator, 'session') as session:
            res = self.paginator.call({})
            self.assertEqual(res, session.get().json())

    def test_iter(self):
        """ It should iterate until the end & yield data. """
        with mock.patch.object(self.paginator, 'call') as call:
            call.side_effect = self.test_responses
            res = list(self.paginator)
            expect = [{'page': 1}, {'page': 2}, {'page': 3}]
            self.assertEqual(res, expect)
