from django.utils.text import slugify
from time import time
from django.core.paginator import Paginator


def post_slugifier(s):
    slugified = slugify(s, allow_unicode=True)
    return slugified + str(int(time()))


def tag_slugifier(title):
    return slugify(title, allow_unicode=True)


def paginate(page_number, queryset, page_size):
    paginator = Paginator(queryset, page_size)
    paginated_data = paginator.get_page(page_number)
    return paginated_data
