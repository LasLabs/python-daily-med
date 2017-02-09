# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import requests


class RequestPaginator(object):
    """ RequestPaginator provides an iterator based upon an initial request.
    """

    PAGE_SIZE = 'pagesize'
    PAGE_NUM = 'page'
    PAGE_TOTAL = 'total_pages'
    PAGE_CURRENT = 'current_page'
    PAGE_DATA = 'data'
    PAGE_META = 'metadata'

    SSL_VERIFY = True

    def __init__(self, endpoint, params=None, page_size=25, page_start=1,
                 output_type=dict,
                 ):
        """ It initializes the RequestPaginator object.

        Args:
            endpoint (str): URI endpoint to call.
            params (dict|bytes): Data to be sent in the query string
                for the Request.
            page_size (int): Size of pages to iterate.
            page_start (int): Page number to start on.
            output_type (type): Class type to output. Object will be
                instantiated using the current row before output.
        """
        self.endpoint = endpoint
        self.params = params
        self.page_size = page_size
        self.page_start = page_start
        self.session = requests.Session()
        self.output_type = output_type

    def __iter__(self, page_num=None):
        """ It provides an iterator for the remote request.

        The result is returned as an instantiated `self.output_type`.
        """

        params = self.params.copy()
        page_num = page_num or self.page_start
        params.update({
            self.PAGE_SIZE: self.page_size,
            self.PAGE_NUM: page_num,
        })
        result = self.call(params)
        meta = result[self.PAGE_META]
        data = result[self.PAGE_DATA]
        for row in data:
            yield self.output_type(**row)
        if meta[self.PAGE_CURRENT] != meta[self.PAGE_TOTAL]:
            for inner_row in self.__iter__(page_num + 1):
                yield inner_row
        else:
            raise StopIteration()

    def call(self, params):
        """ It calls the remote endpoint and returns the JSON decoded result.
        """
        response = self.session.get(
            url=self.endpoint,
            params=params,
            verify=self.SSL_VERIFY,
        )
        return response.json()
