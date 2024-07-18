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

    path('article1/', views.user_login, name='article1'),
    path('article2/', views.user_login, name='article2'),
    path('article3/', views.user_login, name='article3'),
    path('contact/', views.user_login, name='contactus'),
    path('search/', views.user_login, name='search_results'),  # Route for search results

]
