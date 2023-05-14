from django.urls import path
from .views import *

urlpatterns = [
    path('',intro_page, name="intro-page"),
    path('register/',register_page, name="register-page"),
    path('login/',login_page, name="login-page"),
    path('logout/',logout_page, name="logout-page"),
    path('project_detail/',project_detail, name="project-detail-page"),
    path('profile/',profile_page, name="profile-page"),
    path('check_user/',check_user, name="check-user"),
    path('phone_verify/',phone_number_verify, name="phone-verify"),
    path('edit_profile/',edit_profile, name="edit-profile-page"),
    path('edit_password/',edit_password, name="edit-password-page"),
    path('order/',order, name="order-page"),
    path('done_order/',done_order, name="done-order-page"),
    path('my_order/',my_orders, name="my-order-page"),
    path('forgot_password/',forgot_password, name="forgot-password-page"),
    path('project_detail/<int:pk>',project_detail, name="project-detail-page"),

]