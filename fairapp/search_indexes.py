from haystack import indexes
from .models import Project
from django.utils import timezone

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    # template_name="search/Project_text.txt"
    text = indexes.CharField(document=True, use_template=True)
    project_name = indexes.CharField(model_attr='project_name')
    content = indexes.CharField(model_attr='content')
    brief_summary = indexes.CharField(model_attr='brief_summary')


    def get_model(self):
        return Project

   # def index_queryset(self, using=None):
      #  return self.get_model().objects.all()

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(pub_date__lte=timezone.now())
