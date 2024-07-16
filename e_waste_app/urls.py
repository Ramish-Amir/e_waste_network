from django.urls import path
from e_waste_app import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
]
