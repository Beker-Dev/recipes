from rest_framework.pagination import PageNumberPagination


# Making my own recipe pagination (not generic)
class RecipePaginationV2(PageNumberPagination):
    page_size = 9
