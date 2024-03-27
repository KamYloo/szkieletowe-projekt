from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_course/", views.create_course, name="create-course"),
    path('enroll/<int:course_id>/', views.enroll_to_course, name='enroll_to_course'),
    path("courses/", views.courses, name="courses"),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/addtopic', views.add_topic, name='add-topic'),
    path('course/<int:course_id>/participants', views.course_participants, name='course_participants'),
    path('course/<int:course_id>/topic/<int:topic_id>/update/', views.update_topic, name='topic-update'),
    path('course/<int:course_id>/topic/<int:topic_id>/create_assignments/', views.create_assignments, name='create-assignments'),
    path('course/<int:course_id>/assignment/<int:assignment_id>/update/', views.update_assignment, name='assignment-update'),
    path('course/<int:course_id>/assignment/<int:assignment_id>/remove/', views.remove_assignment, name='assignment-remove'),
    path('course/<int:course_id>/assignment/<int:assignment_id>/rate/', views.rate_assignment, name='assignment-rate'),
    path('course/<int:course_id>/assignment/<int:assignment_id>/rate/<int:submission_id>/', views.rate_users_assignment, name='assignment-rate-by-user'),
    path('course/<int:course_id>addfile/<int:topic_id>', views.add_file, name='add-file'),
    path('course/<int:course_id>/deletefile/<str:file_id>/', views.delete_file, name='delete-file'),
    path('assignment/<int:assignment_id>/', views.submit_assignment, name='assignment-submit'),
]




