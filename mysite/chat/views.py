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
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chat_message_thread').order_by('timestamp')
    users = User.objects.all()
    context = {'Threads': threads, 'Users': users}

    return render(request, 'chat/chat.html', context)

@login_required
def create_thread(request, pk):
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
    thread = Thread.objects.get(pk=thread_id)
    thread.delete()
    messages.success(request, "Deleted thread_chat")
    return redirect('chat')

@login_required
def search_thread(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        res = None
        users = request.POST.get('users')
        qs = User.objects.filter(Q(first_name__icontains=users) | Q(last_name__icontains=users))
        if len(qs) > 0 and len(users) > 0:
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
            res = 'No users found...'
        return JsonResponse({'data': res})
    return JsonResponse({})