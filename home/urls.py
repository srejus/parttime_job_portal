from django.urls import path
from .views import *

urlpatterns = [
    path('',IndexView.as_view()),
    path('add-review/<int:id>',AddReviewView.as_view()),
]