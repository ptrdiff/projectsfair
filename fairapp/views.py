from django.views import generic
from .models import Project
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class IndexView(generic.ListView):
    template_name = 'fairapp/index.html'
    context_object_name = 'latest_project_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Project.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Project
    template_name = 'fairapp/details.html'


class ProjectCreate(CreateView):
    model = Project
    fields = '__all__'


class ProjectUpdate(UpdateView):
    model = Project
    fields = '__all__'


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('fairapp:index')
