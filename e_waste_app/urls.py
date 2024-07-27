from e_waste_app import views
from e_waste_app.views import UserRegisterView, LandingPageView, ActivateAccountView
from django.contrib.auth.views import PasswordResetDoneView
from e_waste_app.views import CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from django.urls import path
from e_waste_app.views import (
    HomeView,
    AboutUsView,
    ContactUsView,
)

app_name = 'e_waste_app'
urlpatterns = [
    path(r'', views.HomeView.as_view(), name='home'),
    path(r'login/', views.user_login, name='login'),
    #path(r'register/', views.user_register, name='register'),
    path(r'register/', UserRegisterView.as_view(), name='register'),
    path(r'landing_page/', LandingPageView.as_view(), name='landing'),

    path(r'activate/<uidb64>/<token>/',ActivateAccountView.as_view(),name='activate'),

    path(r'logout/', views.user_logout, name='logout'),
    path(r'password_reset/', views.password_reset, name='password_reset'),
    path(r'password_reset_done', PasswordResetDoneView.as_view(template_name='e_waste_app/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path(r'reset/done/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),
    path('contact/', ContactUsView.as_view(), name='contactus'),
    path('profile/', views.profile, name='profile'),

    # Recycle items urls
    path('add_recycle_item/', views.add_recycle_item, name='add_recycle_item'),
    path('recycle_items/', views.view_recycle_items, name='view_recycle_items'),
    path('my_items/', views.view_my_items, name='view_my_items'),
    path('mark_unavailable/<int:pk>/', views.mark_as_unavailable, name='mark_unavailable'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),
    path('edit_item/<int:pk>/', views.edit_item, name='edit_item'),
    path('item/<int:pk>/', views.recycle_item_detail, name='recycle_item_detail'),

    path('feedback/', views.feedback_view, name='feedback'),

    # Article URLs
    path('articles/', views.article_list_view, name='article_list'),
    path('articles/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('articles/create/', views.article_create_view, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_update_view, name='article_update'),
    path('articles/<int:pk>/delete/', views.article_delete_view, name='article_delete'),
    path('member_articles/', views.member_articles, name='member_articles'),

    path('dashboard/', views.dashboard, name='dashboard'),
]
