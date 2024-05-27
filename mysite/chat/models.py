from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.files.storage import default_storage

class ThreadManager(models.Manager):
    """
       Manager wątków czatu odpowiedzialny za dostęp do danych wątków.

       Metody:
           by_user(self, **kwargs): Zwraca wątki czatu, w których użytkownik jest uczestnikiem.

    """
    def by_user(self, **kwargs):
        """
               Zwraca wątki czatu, w których użytkownik jest uczestnikiem.

               Argumenty:
                   **kwargs: Argumenty nazwane, w tym użytkownik (user), dla którego zwracane są wątki.

               Zwraca:
                   QuerySet: Zbiór wątków czatu zawierających użytkownika.

               Opis działania:
                   Metoda ta pobiera użytkownika przekazanego jako argument nazwany 'user'.
                   Następnie buduje zapytanie (QuerySet), które wybiera wątki czatu, gdzie
                   użytkownik jest jednym z uczestników (pierwsza lub druga osoba w wątku).
                   Zapytanie jest filtrowane i zwracane, a także usuwane duplikaty wątków
                   przy użyciu metody 'distinct()'.
        """
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        q = self.get_queryset().filter(lookup).distinct()
        return q

class Thread(models.Model):
    """
       Model reprezentujący wątek czatu między dwoma użytkownikami.

       Atrybuty:
           first_person (ForeignKey): Pierwszy użytkownik w wątku.
           second_person (ForeignKey): Drugi użytkownik w wątku.
           updated (DateTimeField): Data i czas ostatniej aktualizacji wątku.
           timestamp (DateTimeField): Data i czas utworzenia wątku.
           objects (ThreadManager): Menedżer dostępu do danych wątków.

       Meta:
           unique_together (tuple): Unikalna para użytkowników w wątku.

    """
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ThreadManager()
    class Meta:
        unique_together = ('first_person', 'second_person')


class ChatMessage(models.Model):
    """
        Model reprezentujący pojedynczą wiadomość w wątku czatu.

        Atrybuty:
            thread (ForeignKey): Wątek, do którego należy ta wiadomość.
            user (ForeignKey): Użytkownik, który wysłał tę wiadomość.
            message (TextField): Treść wiadomości.
            timestamp (DateTimeField): Data i czas wysłania wiadomości.

    """
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_message_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)