from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Education, EduInst, EduProg, Skill, Activity
from django.contrib.auth.models import User


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
        fields = ('middle_name', 'phone')


class EducationForm (forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'

    '''def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        self.fields["edu"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["edu"].help_text = ""
        self.fields["edu"].queryset = EduInst.objects.all()
        self.fields["prog"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["prog"].help_text = ""
        self.fields["prog"].queryset = EduProg.objects.all()
        self.fields["year"].widget = forms.widgets.NumberInput()'''
