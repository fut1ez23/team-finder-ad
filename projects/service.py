from django.core.paginator import Paginator

from projects.constants import PAGE_SIZE


def paginate(queryset, page_number, page_size=PAGE_SIZE):
    paginator = Paginator(queryset, page_size)
    return paginator.get_page(page_number)


def build_query_prefix(request, exclude=("page",)):
    params = request.GET.copy()
    for key in exclude:
        params.pop(key, None)
    encoded = params.urlencode()
    return f"{encoded}&" if encoded else ""

