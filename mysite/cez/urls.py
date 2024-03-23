from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("assignment/", views.AssignmentListView.as_view(), name="assignment"),
    path('assignment/<int:assignment_id>/', views.submit_assignment, name='assignment-submit'),
]