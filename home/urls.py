from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employees/', views.employees, name='employees'),
    path('management/', views.management, name='management'),
    path('department/', views.department, name='department'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('delete_employees/<int:employee_id>/', views.delete_employees, name='delete_employees'),
    path('calendar/<int:employee_id>/', views.calendar_view, name='calendar'),
    path('get_user_data/<int:employee_id>', views.get_calendar_data, name="get_calendar_data"),
    path('set_user_event/<int:employee_id>', views.set_employee_event, name="set_employee_event"),
    path('update_event/', views.update_event, name="update_event")
]
