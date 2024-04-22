from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat, name="chat"),
    path("chat/search/", views.search_thread, name="search"),
    path("chat/create_thread/<int:pk>/", views.create_thread, name="create_thread_chat"),
    path('chat/remove_thread/<int:thread_id>/', views.delete_thread, name='delete_thread'),
]




