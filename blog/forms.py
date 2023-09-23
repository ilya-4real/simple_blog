from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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
        fields = ['title', 'slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Title of the post'}),
            'slug': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'slug'}),
            'body': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Body'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select mb-3'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('You cannot create post with slug "create"')
        return new_slug


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput({'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput({'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput({'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput({'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserLogInForm(AuthenticationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
