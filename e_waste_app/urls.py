from e_waste_app import views
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

from e_waste_app.forms import PasswordResetConfirmForm
from .views import CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, feedback_view
from .views import CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, feedback_view
from django.contrib.auth.views import PasswordResetDoneView
from e_waste_app.views import CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from django.urls import path
from e_waste_app.views import (
    HomeView,
    AboutUsView,
    Article1View,
    Article2View,
    Article3View,
    ContactUsView,    # Import other views as needed
)

app_name = 'e_waste_app'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='e_waste_app/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('article1/', Article1View.as_view(), name='article1'),
    path('article2/', Article2View.as_view(), name='article2'),
    path('article3/', Article3View.as_view(), name='article3'),
    path('contact/', ContactUsView.as_view(), name='contactus'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_results, name='search_results'),

    # Recycle items urls
    path('add_recycle_item/', views.add_recycle_item, name='add_recycle_item'),
    path('recycle_items/', views.view_recycle_items, name='view_recycle_items'),
    path('my_items/', views.view_my_items, name='view_my_items'),
    path('mark_unavailable/<int:pk>/', views.mark_as_unavailable, name='mark_unavailable'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('edit_item/<int:pk>/', views.edit_item, name='edit_item'),
    path('item/<int:pk>/', views.recycle_item_detail, name='recycle_item_detail'),
    path('feedback/', views.feedback_view, name='feedback'),
]
