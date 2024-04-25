from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from chat.models import Thread
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

@login_required
def chat(request):
    """
       Widok odpowiedzialny za wyświetlanie panelu czatu.

       Wymagane uprawnienia:
           - Użytkownik musi być zalogowany.

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.

       Zwraca:
           HttpResponse: Odpowiedź HTTP zawierająca panel czatu.

       Opis działania:
           Ten widok pobiera wątki czatu dla zalogowanego użytkownika, uporządkowane
           według czasu dodania. Dodatkowo pobiera listę wszystkich użytkowników.
           Następnie przekazuje te dane do szablonu 'chat/chat.html', gdzie zostaną
           wyświetlone.

       Wyjątki:
           None

       Przykład użycia:
           # Przykład użycia widoku w pliku urls.py:
           # path('czat/', views.chat, name='czat'),

       """
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chat_message_thread').order_by('timestamp')
    users = User.objects.all()
    context = {'Threads': threads, 'Users': users}

    return render(request, 'chat/chat.html', context)

@login_required
def create_thread(request, pk):
    """
        Widok odpowiedzialny za tworzenie nowego wątku czatu między użytkownikami.

        Wymagane uprawnienia:
            - Użytkownik musi być zalogowany.

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.
            pk (int): Identyfikator (primary key) innego użytkownika, z którym ma zostać utworzony wątek.

        Zwraca:
            HttpResponse: Przekierowanie do panelu czatu lub komunikat o błędzie.

        Opis działania:
            Ten widok najpierw sprawdza, czy istnieje już wątek czatu między aktualnym
            użytkownikiem a innym użytkownikiem o podanym identyfikatorze (pk). Jeśli taki
            wątek istnieje, użytkownik zostaje przekierowany do panelu czatu, a wyświetlany
            jest komunikat o istniejącym już wątku czatu. W przeciwnym przypadku tworzony
            jest nowy wątek czatu między użytkownikami i użytkownik zostaje przekierowany
            do panelu czatu.

        Wyjątki:
            None

        Przykład użycia:
            # Przykład użycia widoku w pliku urls.py:
            # path('utworz-watek/<int:pk>/', views.create_thread, name='utworz_watek'),

        """
    other_user  = get_object_or_404(User, pk=pk)
    thread = Thread.objects.filter(
        Q(first_person=request.user, second_person=other_user) |
        Q(first_person=other_user, second_person=request.user)
    ).first()

    if thread:
        messages.error(request, 'The chat thread already exists')
        return redirect('chat')

    new_thread = Thread.objects.create(first_person=request.user, second_person=other_user)
    return redirect('chat')

@login_required
def delete_thread(request, thread_id):
    """
       Widok odpowiedzialny za usuwanie wątku czatu.

       Wymagane uprawnienia:
           - Użytkownik musi być zalogowany.

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.
           thread_id (int): Identyfikator (primary key) wątku czatu do usunięcia.

       Zwraca:
           HttpResponse: Przekierowanie do panelu czatu po usunięciu wątku.

       Opis działania:
           Ten widok pobiera wątek czatu na podstawie podanego identyfikatora.
           Następnie usuwa ten wątek. Po usunięciu wątku, wyświetlany jest komunikat
           o sukcesie, a użytkownik zostaje przekierowany do panelu czatu.

       Wyjątki:
           None

       Przykład użycia:
           # Przykład użycia widoku w pliku urls.py:
           # path('usun-watek/<int:thread_id>/', views.delete_thread, name='usun_watek'),

       """
    thread = Thread.objects.get(pk=thread_id)
    thread.delete()
    messages.success(request, "Deleted thread_chat")
    return redirect('chat')

@login_required
def search_thread(request):
    """
        Widok odpowiedzialny za wyszukiwanie użytkowników do rozpoczęcia nowego wątku czatu.

        Wymagane uprawnienia:
            - Użytkownik musi być zalogowany.

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.

        Zwraca:
            JsonResponse: Dane użytkowników pasujących do kryteriów wyszukiwania w formacie JSON.

        Opis działania:
            Ten widok obsługuje zapytania AJAX wysyłane podczas wyszukiwania użytkowników
            do rozpoczęcia nowego wątku czatu. Sprawdza, czy żądanie jest zapytaniem AJAX.
            Następnie pobiera dane wyszukiwanych użytkowników na podstawie wartości przekazanej
            w polu formularza 'users'. Jeśli znalezione są pasujące użytkownicy, ich dane
            są zwracane w formacie JSON, w przeciwnym razie zwracany jest komunikat o braku
            znalezionych użytkowników.

        Wyjątki:
            None

        Przykład użycia:
            # Przykład użycia widoku w pliku JavaScript:
            # $.ajax({
            #     url: '/szukaj-watek/',
            #     type: 'POST',
            #     data: {users: 'nazwa_uzytkownika'},
            #     success: function(data) {
            #         // Obsługa zwróconych danych
            #     }
            # });

        """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = None
        users = request.POST.get('users')
        if users is not None and users != '':
            qs = User.objects.filter(Q(first_name__icontains=users) | Q(last_name__icontains=users))
            if len(qs) > 0:
                data = []
                for user in qs:
                    item = {
                        'pk': user.pk,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'avatar': user.profile.profile_pic.url
                    }
                    data.append(item)
                res = data
            else:
                res = "No Users Found...".format(users)
        else:
            res = []
        return JsonResponse({'data': res})
    return JsonResponse({})