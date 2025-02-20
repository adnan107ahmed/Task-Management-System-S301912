from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('projects_list/', views.projects_list, name='projects_list'),
    path('task/create/', views.create_or_update_task, name='create_task'),
    path('task/<int:task_id>/', views.create_or_update_task, name='update_task'), 
    path('<int:project_id>/', views.home, name='project_tasks'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete_project/<int:project_id>', views.delete_project, name="delete_project"),
    path('create_project/', views.create_or_update_project, name='create_project'),
    path('edit_project/<int:project_id>/', views.create_or_update_project, name='edit_project'),

]
