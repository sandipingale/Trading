from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name="registrations/password_reset_form.html",
                                              email_template_name="registrations/password_reset_email.html"),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registrations/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registrations/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registrations/password_reset_complete.html"),
         name='password_reset_complete'),
]

