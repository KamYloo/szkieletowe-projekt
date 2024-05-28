from django.urls import path
from . import views

urlpatterns = [
    # Ścieżka do panelu czatu
    path("chat/", views.chat, name="chat"),

    # Ścieżka do wyszukiwania użytkowników dla nowego wątku czatu
    path("chat/search/", views.search_thread, name="search"),

    # Ścieżka do tworzenia nowego wątku czatu z określonym użytkownikiem
    path("chat/create_thread/<int:pk>/", views.create_thread, name="create_thread_chat"),

    # Ścieżka do usuwania wątku czatu
    path('chat/remove_thread/<int:thread_id>/', views.delete_thread, name='delete_thread'),
]




