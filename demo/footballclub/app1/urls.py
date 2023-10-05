from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index, name="index"),
    path('registration', views.reg, name="registration"),
    path('login', views.login, name="login"),
    path('staff',views.staff,name="staff"),
    path('player',views.player,name="player"),
    path('coach',views.coach,name="coach"),
    path('logout',views.logout,name="logout"),
    path('accounts/login/',views.login,name="login"),
    path('adminreg',views.adminreg,name="adminreg"),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

