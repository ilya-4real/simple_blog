from django.utils.text import slugify
from time import time
from django.core.paginator import Paginator


def title_to_slug(s):
    slugified = slugify(s, allow_unicode=True)
    return slugified + str(int(time()))


def paginate(objects, pages: int):
    paginator = Paginator(objects, pages)
    ...


