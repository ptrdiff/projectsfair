from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('project_name', 'pub_date', ('start_date', 'end_date'), 'head', 'brief_summary', 'content',
                  'app_deadline', 'num_places', 'type',)
