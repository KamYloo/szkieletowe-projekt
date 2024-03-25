from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("topic/", views.TopicListView.as_view(), name="topic"),
    path('topic/<int:topic_id>/', views.view_topic, name='topic-detail'),
    path('topic/<int:topic_id>/update/', views.update_topic, name='topic-update'),
    path('topic/<int:topic_id>/create_assignments/', views.create_assignments, name='create-assignments'),
    path("courses/", views.course, name="courses"),
    path("create_course/", views.create_course, name="create-course"),
    path("assignment/", views.AssignmentListView.as_view(), name="assignment"),
    path('assignment/<int:assignment_id>/', views.submit_assignment, name='assignment-submit'),
    path('assignment/<int:assignment_id>/update/', views.update_assignment, name='assignment-update'),
    path('addfile/<int:topic_id>', views.add_file, name='add-file'),
    path('topic/<int:topic_id>/deletefile/<str:file_id>', views.delete_file, name='delete-file')
]