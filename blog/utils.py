from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from .models import *


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.filter(slug__iexact=slug).select_related('author')[0]
        return render(request, self.template, context={self.model.__name__.lower(): obj})


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            obj = bound_form.save(commit=False)
            obj.author = request.user
            obj.save()
            bound_form.save_m2m()
            return redirect(obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    object_form = None
    model = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        if request.user != obj.author:
            return redirect('home_page_url')
        bound_form = self.object_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.object_form(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    delete_template = None
    list_template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        if request.user != obj.author:
            return redirect('home_page_url')
        return render(request, self.delete_template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.list_template))
