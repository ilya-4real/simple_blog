from django.utils.text import slugify
from time import time
from django.core.paginator import Paginator


def title_to_slug(s):
    slugified = slugify(s, allow_unicode=True)
    return slugified + str(int(time()))


def paginate(page_number, queryset, page_size):
    paginator = Paginator(queryset, page_size)
    paginated_data = paginator.get_page(page_number)
    return paginated_data
