from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Profile, AppForProject
from django.contrib.auth.models import User
from django.db import transaction


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('project_name', 'pub_date', 'start_date', 'end_date', 'head', 'brief_summary', 'content',
                  'app_deadline', 'num_places', 'type', 'tag', 'skill')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('interests', 'achievements', 'faculty', 'status', 'grade')
