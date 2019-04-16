from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.files.storage import Storage


class Default_Paginations(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 5


class Newlist_Paginations(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {'counts': self.page.paginator.count,
             'data': data,
             'page': self.page.number,
             'total_page': self.page.paginator.num_pages,
             'pagesize': self.get_page_size(self.request)
             })