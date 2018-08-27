from haystack import indexes
from .models import Project


class ProjectIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/book_text.txt")
    project_name = indexes.CharField(model_attr=' project_name')
    content = indexes.CharField(model_attr=' content')


    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.all()