from . import views
from django.urls import include, path

app_name = 'fairapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create/', views.ProjectCreate.as_view(), name='project_create'),
    path('<int:pk>/update/', views.ProjectUpdate.as_view(), name='project_update'),
    path('<int:pk>/delete/', views.ProjectDelete.as_view(), name='project_delete'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
]
