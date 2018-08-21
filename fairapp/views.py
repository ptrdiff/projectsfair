from django.views import generic
from .models import Project
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from fairapp.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .filters import ProjectFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request, page = 1):
    object_list = Project.objects.all()
    paginator = Paginator(object_list, 10)
    if page > paginator.num_pages:
        page = 1
    try:
        projects = paginator.get_page(page)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request,'fairapp/index.html',{'page': page,
                                                'projects': projects,
                                                })

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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('fairapp:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def search(request):
    project_list = Project.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=project_list)
    return render(request, 'fairapp/search_projects.html', {'filter': project_filter})
