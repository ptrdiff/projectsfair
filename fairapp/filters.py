from .models import Project, Profile
import django_filters


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = '__all__'

class SkillFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = '__all__'