from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index, name="index"),
    path('registration', views.reg, name="registration"),
    path('check_email/', views.check_email, name='check_email'),
    path('validate_email/', views.validate_email, name='validate_email'),
    path('checkJerseyNumberAvailability/', views.checkJerseyNumberAvailability, name='checkJerseyNumberAvailability'),
    path('login', views.login, name="login"),
    path('demo', views.demo, name="demo"),



    path('staff',views.staff,name="staff"),
    path('staffprofile',views.staffprofile,name="staffprofile"),
    path('staffupdate',views.staffupdate,name="staffupdate"),
    path('staffpayment',views.staffpayment,name="staffpayment"),
    path('process_payment/', views.process_payment, name='process_payment'),



    path('admin1',views.admin1,name="admin1"),
    path('navigate_to_page', views.navigate_to_page, name='navigate_to_page'),    
    path('adminindex',views.adminindex,name="adminindex"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('player',views.player,name="player"),
    path('player2',views.player2,name="player2"),
    path('player_profile/', views.player_profile, name='player_profile'),
    path('playerupdate',views.playerupdate,name="playerupdate"),
    path('playerchat',views.playerchat,name="playerchat"),
    path('training_list1', views.training_list1, name="training_list1"),
    path('playertraining',views.playertraining,name='playertraining'),
    path('generate_training_pdf/', views.generate_training_pdf_view, name='generate_training_pdf'),

    path('playerperformance', views.playerperformance, name='playerperformance_no_id'),  # Rename the URL
    path('playerperformance/<str:player_id>/', views.playerperformance, name='playerperformance'),
    path('create_venue/', views.create_venue, name='create_venue'),




    path('coach/',views.coach,name="coach"),
    path('coachprofile',views.coachprofile,name="coachprofile"),
    path('coachupdate',views.coachupdate,name="coachupdate"),
    path('coachchat',views.coachchat,name="coachchat"),
    path('coachaddtraining',views.coachaddtraining,name="coachaddtraining"),
    path('training_list', views.training_list, name="training_list"),
    path('training_list/<int:training_id>/', views.training_list, name="training_list"),
    path('update_performance/<int:training_id>/', views.update_performance, name='update_performance'),

    
    
    path('logout',views.logout,name="logout"),
    path('match_list2/logout',views.logout,name="logout"),
    path('accounts/login/',views.login,name="login"),
    path('adminreg',views.adminreg,name="adminreg"),
    
    path('opponent/delete/<int:opponent_id>/', views.delete_opponent, name='delete_opponent'),
    path('admin_opponent_list',views.admin_opponent_list,name="admin_opponent_list"),
    path('add_opponent',views.add_opponent,name="add_opponent"),
    path('add_match_schedule',views.add_match_schedule,name="add_match_schedule"),
    path('match_list/', views.match_list, name='match_list'),
    path('match_list1/', views.match_list1, name='match_list1'),
    path('match_list2/player_profile', views.player_profile, name='player_profile'),

    path('match_list2/', views.match_list2, name='match_list2'),


     path('update_result/<int:match_id>/', views.update_result, name='update_result'),




    path('delete_user/<str:user_email>/', views.delete_user, name='delete_user'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('api/chat/start/', views.ChatStart.as_view(), name='chat-start'),
    path('match_list2/logout', views.logout, name="logout"),


      
    path('scout',views.scout, name="scout"),
    path('scoutplayer',views.scoutplayer, name="scoutplayer"),
    path('scout_reg',views.scout_reg, name="scout_reg"),
    path('scout_profile',views.scout_profile, name="scout_profile"),
    path('chat/<int:receiver_id>/', views.chat, name='chat'),
    path('send_message/', views.send_message, name='send_message'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
