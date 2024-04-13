from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat, name="chat"),
    path("chat/search/", views.search_thread, name="search"),
    path("chat/<pk>/", views.create_thread, name="create_thread_chat"),
    path('chat/<int:thread_id>/remove/', views.delete_thread, name='delete_thread'),
]




