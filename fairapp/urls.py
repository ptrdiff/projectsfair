from . import views
from django.urls import include, path

app_name = 'fairapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>/', views.index, name='index'),
    path('projects/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('projects/create/', views.ProjectCreate.as_view(), name='project_create'),
    path('projects/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project_delete'),
    path('signup/', views.signup, name='signup'),
    path('projects/search/', views.index, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile')
]
