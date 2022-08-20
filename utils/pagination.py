import math
from django.core.paginator import Paginator
from django.core.handlers.wsgi import WSGIRequest


def make_pagination_range(page_range: list, amount_pages: int, current_page: int = 1) -> dict:
    middle_range = math.ceil(amount_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'amount_pages': amount_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request: WSGIRequest, iterable: list | tuple, per_page: int = 3) -> tuple:
    paginator = Paginator(iterable, per_page)
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    pagination_range = make_pagination_range(
        page_range=paginator.page_range,
        amount_pages=per_page,
        current_page=int(page_number),
    )
    return page_object, pagination_range
