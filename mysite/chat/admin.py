from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Thread, ChatMessage

admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    """
        Klasa Inline dla modelu ChatMessage, umożliwiająca edycję wiadomości czatu
        bezpośrednio z widoku modelu Thread w panelu administracyjnym.
    """
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    """
        Klasa reprezentująca niestandardowy panel administracyjny dla modelu Thread.

        Atrybuty:
            inlines (list): Lista Inline dla modelu Thread, w tym ChatMessageInline.

    """
    inlines = [ChatMessage]
    class Meta:
        """
                Klasa Meta definiująca model dla panelu administracyjnego.
        """
        model = Thread

# Rejestracja niestandardowego panelu administracyjnego dla modelu Thread
admin.site.register(Thread, ThreadAdmin)