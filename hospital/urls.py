from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('', views.index, name='index'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('patients/', views.patients, name='patients'),
    path('registrations/', views.registrations, name='registrations'),
    path('registrations/<int:pk>/action/', views.registration_action, name='registration_action'),
    path('records/', views.records, name='records'),
]
