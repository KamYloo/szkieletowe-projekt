from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("courses/", views.course, name="courses"),
    path("create_course/", views.create_course, name="create-course"),
    path("assignment/", views.AssignmentListView.as_view(), name="assignment"),
    path('assignment/<int:assignment_id>/', views.submit_assignment, name='assignment-submit'),
]