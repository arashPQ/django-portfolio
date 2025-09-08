from django.urls import path

from . import views

app_name = 'developer'

urlpatterns = [
    path('', views.portfolio, name='index'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail')
]