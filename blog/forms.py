from django import forms

from .models import *
from django.core.exceptions import ValidationError


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-3', 'placeholder': 'tag name'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('You cannot create "create" tag!')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('This tag already exists!')
        return new_slug

    def clean_title(self):
        new_title = self.cleaned_data['title']
        if " " in new_title:
            raise ValidationError('You can create only one-word tag')
        return new_title


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Title of the post'}),
            'body': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Body'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select mb-3'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('You cannot create post with slug "create"')
        return new_slug


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'leave comment', 'rows': '3'})
        }



