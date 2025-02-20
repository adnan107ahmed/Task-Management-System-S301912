from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('create_project/', views.create_project, name='create_project'),
    path('task/create/', views.create_or_update_task, name='create_task'),
    path('task/<int:task_id>/', views.create_or_update_task, name='update_task'), 
    path('<int:project_id>/', views.home, name='project_tasks'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),

]
