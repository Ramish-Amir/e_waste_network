from e_waste_app import views
from django.urls import path
app_name = 'e_waste_app'

urlpatterns =[
    path(r'', views.home, name='home'),
    path(r'login/', views.user_login, name='login'),
    path(r'register/', views.user_register, name='register'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'password_reset/', views.password_reset, name='password_reset'),
    path(r'password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('article1/', views.article1, name='article1'),
    path('article2/', views.article2, name='article2'),
    path('article3/', views.article3, name='article3'),
    path('contact/', views.contact_us, name='contactus'),
    path('search/', views.search_results, name='search_results'),  # Route for search results
    path('post_request/', views.post_recycling_request, name='post_recycling_request'),
    path('search_requests/', views.search_recycling_requests, name='search_recycling_requests'),
]
