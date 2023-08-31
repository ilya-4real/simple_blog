from django.shortcuts import redirect


def redirect_blog(request):
    return redirect('home_page_url', permanent=True)
