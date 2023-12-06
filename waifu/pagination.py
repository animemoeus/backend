from rest_framework.pagination import PageNumberPagination


class WaifuListPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 50
    page_size_query_param = "count"
