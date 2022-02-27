from rest_framework.pagination import PageNumberPagination


class PageNumberPaginator(PageNumberPagination):
    page_size = 6
