from django.http import HttpResponseRedirect
from django.views import generic
from .models import Project, AppForProject, Skill
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from fairapp.forms import SignUpForm, SkillForm, ActivityForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .filters import ProjectFilter
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils import six
from django.apps import apps
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.views.generic.edit import ModelFormMixin

def and_filter(project_list, request, *fieldtofilter):
    q_dict = dict(six.iterlists(request.GET))
    for field in fieldtofilter:
        project_list2 = []

        if field not in q_dict:
            continue

        field_attribute = q_dict.get(field)
        etalon=[]
        for s in field_attribute:
            etalon.append(apps.get_model('fairapp', field).objects.get(pk=s))

        length = len(project_list)
        for p in range(length):
            attr = getattr(project_list[p], field)

            if set(list(attr.all()))&set(etalon) == set(etalon):
                project_list2.append(project_list[p])

        if len(project_list2) > 0:
            project_list = project_list2
    return project_list


def index(request, page=1):
    object_list = Project.objects.all().exclude(status__in=['m', 'r'])
    project_filter = ProjectFilter(request.GET, queryset=object_list)
    project_list = and_filter(project_filter.qs, request, 'skill', 'tag')

    paginator = Paginator(project_list, 5)
    if page > paginator.num_pages:
        page = 1
    try:
        projects = paginator.get_page(page)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/index.html', {'page': page,
                                                  'projects': projects,
                                                  'filter': project_filter,
                                                  })


@login_required
def view_profile_projects(request, page=1):
    project_list = Project.objects.all().filter(members__in=[request.user.id])
    paginator = Paginator(project_list.order_by('-date_start'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        projects = paginator.get_page(page)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/myprojects.html', {'page': page,
                                                       'projects': projects,
                                                       })


@login_required
def view_profile_applications(request, page=1):
    object_list = AppForProject.objects.all().filter(user__in=[request.user])
    paginator = Paginator(object_list.order_by('-id'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        apps = paginator.get_page(page)
    except EmptyPage:
        apps = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/myapplications.html', {'page': page,
                                                           'apps': apps,
                                                           })


@permission_required('fairapp.approve_project')
def moderator_index(request, page=1):
    object_list = Project.objects.all().filter(status='m')
    paginator = Paginator(object_list.order_by('-date_req_end'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        projects = paginator.get_page(page)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/moderation_index.html', {'page': page,
                                                             'projects': projects,
                                                             })


@permission_required('fairapp.approve_application')
def moderator_applications(request, page=1):
    object_list = AppForProject.objects.all().filter(status='m')
    paginator = Paginator(object_list.order_by('-id'), 5)
    if page > paginator.num_pages:
        page = 1
    try:
        apps = paginator.get_page(page)
    except EmptyPage:
        apps = paginator.page(paginator.num_pages)
    return render(request, 'fairapp/applications.html', {'page': page,
                                                         'apps': apps,
                                                         })


class ModerDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'fairapp.approve_project'
    model = Project
    template_name = 'fairapp/details.html'


class ModerAppDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'fairapp.approve_application'
    model = AppForProject
    template_name = 'fairapp/moderappdetails.html'


class IndexView(generic.ListView):
    template_name = 'fairapp/index.html'
    context_object_name = 'latest_project_list'

    def get_queryset(self):
        return Project.objects.order_by('date_req_end')[:5]


class DetailView(generic.DetailView):
    model = Project
    template_name = 'fairapp/details.html'

    def dispatch(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs['pk'])
        if project.status in ['m','r']:
            return redirect('fairapp:index')
        return super(DetailView, self).dispatch(request, *args, **kwargs)


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ('name', 'descrip_short', 'descrip_full', 'num_participants', 'date_start',
              'date_end', 'date_req_end', 'tag', 'skill', 'activity')

    def form_valid(self, form):
        form.save()
        form.instance.id_lead.add(self.request.user)
        form.instance.places_left = int(form.instance.num_participants)
        form.save()
        return super(ProjectCreate, self).form_valid(form)


class ProjectUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'fairapp.edit_project'
    model = Project
    fields = '__all__'


class ProjectDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'fairapp.delete_project'
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


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        #skill_form = SkillForm(request.POST, instance=request.user.profile.ap_skill)
        #activity_form = SkillForm(request.POST, instance=request.user.profile.ap_act)

        if user_form.is_valid() and profile_form.is_valid():#\
             #   and skill_form.is_valid() and activity_form.is_valid():
            user_form.save()
            profile_form.save()
            #skill_form.save()
            #activity_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        #skill_form = SkillForm(instance=request.user.profile.ap_skill)
        #activity_form = SkillForm(instance=request.user.profile.ap_act)

    return render(request, 'fairapp/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        #'skill_form': skill_form,
        #'activity_form': activity_form
    })


@login_required
def view_profile(request):
    profile = request.user.profile
    return render(request, 'fairapp/profile.html', {"profile": profile})


class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = AppForProject
    fields = ('covering_letter', )

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            form.instance.project = Project.objects.get(pk=self.kwargs['pk'])
            form.instance.status = 'm'
            form.save()
            return super(ApplicationCreate, self).form_valid(form)
        except IntegrityError as e:
            return render_to_response("fairapp/error.html", {"message": e.args})

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreate, self).get_context_data()
        context['pk'] = self.kwargs['pk']
        return context


@permission_required('fairapp.approve_project')
def approve_project(request, pk):
    obj = Project.objects.get(pk=pk)
    if request.POST['Decision'] == 'approve':
        obj.status = 'c'
    elif request.POST['Decision'] == 'reject':
        obj.status = 'r'
    obj.save()
    return redirect('fairapp:index')


@permission_required('fairapp.approve_application')
def approve_application(request, pk):
    obj = AppForProject.objects.get(pk=pk)
    if request.POST['Decision'] == 'approve':
        obj.project.members.add(obj.user)
        places = obj.project.places_left
        obj.project.places_left = places - 1
        obj.status = 'a'
    elif request.POST['Decision'] == 'reject':
        obj.status = 'r'
    obj.project.save()
    obj.save()
    return redirect('fairapp:index')


class ApplicationView(LoginRequiredMixin, generic.DetailView):
    model = AppForProject
    fields = '__all__'
