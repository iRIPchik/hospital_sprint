from django.urls import path

from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.doctors_list, name='doctors_list'),
    path(
        'doctors/<int:doctor_id>/',
        views.doctor_schedule,
        name='doctor_schedule'
    ),
    path(
        'appointments/create/',
        views.appointment_create,
        name='appointment_create'
    ),
]
