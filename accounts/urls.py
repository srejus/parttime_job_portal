from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('logout',LogoutView.as_view()),
    path('profile',ProfileView.as_view(),name='my_profile'),
    path('profile/<int:id>',ProfileView.as_view(),name='view_profile'),
    path('signup',SignupView.as_view()),
    path('profile/deleteskill/<int:id>',DeleteSkillView.as_view()),

    path('my-job',MyJobView.as_view()),
]