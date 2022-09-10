from rest_framework.pagination import PageNumberPagination


# Making my own recipe pagination (not generic)
class RecipePaginationV1(PageNumberPagination):
    page_size = 9
