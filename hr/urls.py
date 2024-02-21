from django.urls import path
from .views import *

urlpatterns = [
    path('',HrHomeView.as_view()),
    path('jobs',HrJobView.as_view()),
    path('attendence/<int:id>',MarkAttendence.as_view()),
    path('employee',HrEmployeeView.as_view()),
    path('employee/<int:id>',HrEmployeeView.as_view()),
    path('employee/remove/<int:id>',HrRemoveEmployeeView.as_view()),
    path('approve/<int:id>',ApproveView.as_view()),
    path('reject/<int:id>',RejectView.as_view()),
    path('post-job',PostJobView.as_view()),
]