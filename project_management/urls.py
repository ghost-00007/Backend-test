from django.urls import path
from . import views 

urlpatterns = [
    path('department/', views.DepartmentView.as_view(), name='Department'), 
    path('department/<int:pk>/', views.DepartmentView.as_view(), name='Department'),

    path('project/', views.ProjectView.as_view(), name='Project'), 
    path('project/<int:pk>/', views.ProjectView.as_view(), name='Project'),

    path('teams/', views.TeamsView.as_view(), name='Teams'), 
    path('teams/<int:pk>/', views.TeamsView.as_view(), name='Teams'),

    path('designation/', views.DesignationView.as_view(), name='Designation-View'), 
    path('designation/<int:pk>/', views.DesignationView.as_view(), name='Designation-View'),
]

