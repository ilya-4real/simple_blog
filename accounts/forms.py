from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .tasks import send_welcome_email_task
from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'bio', 'profile_image']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'user name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email address'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'bio', 'rows': '3'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control', 'id': 'formFile', 'type': 'file'})
        }


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput({'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput({'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput({'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput({'class': 'form-control'}))

    def send_email(self):
        send_welcome_email_task.delay(self.cleaned_data['email'], self.cleaned_data['username'])

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2')


class UserLogInForm(AuthenticationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
