from django.urls import path
from e_waste_app import views

app_name = 'e_waste_app'

urlpatterns = [
    path(r'', views.index, name='index'),
    path('post_request/', views.post_recycling_request, name='post_recycling_request'),
    path('search_requests/', views.search_recycling_requests, name='search_recycling_requests'),
]
