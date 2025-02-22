from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('projects_list/', views.projects_list, name='projects_list'),
    path('task/create/', views.create_or_update_task, name='create_task'),
    path('task/<int:task_id>/', views.create_or_update_task, name='update_task'), 
    path('<int:project_id>/', views.home, name='project_tasks'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete_project/<int:project_id>', views.delete_project, name="delete_project"),
    path('create_project/', views.create_or_update_project, name='create_project'),
    path('edit_project/<int:project_id>/', views.create_or_update_project, name='edit_project'),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
