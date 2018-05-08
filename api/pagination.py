from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination



class RatingLimitOffestpagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10

class RatingPageNumberPagination(PageNumberPagination):
    page_size = 10