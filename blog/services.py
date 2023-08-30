from django.utils.text import slugify
from time import time


def title_to_slug(s):
    slugified = slugify(s, allow_unicode=True)
    return slugified + str(int(time()))
