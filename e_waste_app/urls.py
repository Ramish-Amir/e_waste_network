from e_waste_app import views
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from e_waste_app.forms import PasswordResetConfirmForm
from e_waste_app.views import CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

app_name = 'e_waste_app'
urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'login/', views.user_login, name='login'),
    path(r'register/', views.user_register, name='register'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'password_reset/', views.password_reset, name='password_reset'),
    path(r'password_reset_done', PasswordResetDoneView.as_view(template_name='e_waste_app/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path(r'reset/done/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('article1/', views.article1, name='article1'),
    path('article2/', views.article2, name='article2'),
    path('article3/', views.article3, name='article3'),
    path('contact/', views.contact_us, name='contactus'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_results, name='search_results'),
    path('add_recycle_item/', views.add_recycle_item, name='add_recycle_item'),
    path(r'recycle_items/', views.view_recycle_items, name='view_recycle_items'),
]
