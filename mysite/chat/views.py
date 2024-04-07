from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.models import Thread


@login_required
def chat(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chat_message_thread').order_by('timestamp')
    context = {'Threads': threads}

    return render(request, 'chat/chat.html', context)