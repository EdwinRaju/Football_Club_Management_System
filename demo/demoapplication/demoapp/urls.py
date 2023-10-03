from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.signin, name="signin"),  # Define the login URL pattern
    path('registration', views.reg, name="registration"),
    path('staff',views.staff,name="staff"),
    path('player',views.player,name="player"),
    path('coach',views.coach,name="coach"),
    path('logout', views.user_logout, name='logout'),
     # Password reset URLs
    path('password_reset', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html'), name='password_reset'),
    path('password_resetdone', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
]