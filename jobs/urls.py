from django.urls import path
from .views import *

urlpatterns = [
    path('<int:id>',FetchJobView.as_view()),
    path('',FetchJobView.as_view()),
    path('apply/<int:id>',ApplyJobView.as_view()),
]