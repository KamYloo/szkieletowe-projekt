import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from chat.models import Thread, ChatMessage

User = get_user_model()

class ChatConsumer(AsyncConsumer):
    """
        Konsumer obsługujący połączenia WebSocket dla czatu.

        Metody:
            websocket_connect(self, event): Metoda wywoływana przy nawiązaniu połączenia WebSocket.
            websocket_receive(self, event): Metoda wywoływana przy otrzymaniu wiadomości WebSocket.
            websocket_disconnect(self, event): Metoda wywoływana przy rozłączeniu połączenia WebSocket.
            chat_message(self, event): Metoda wysyłająca wiadomość czatu do klienta WebSocket.
            get_user_object(self, user_id): Metoda asynchroniczna pobierająca obiekt użytkownika z bazy danych.
            get_thread(self, thread_id): Metoda asynchroniczna pobierająca obiekt wątku z bazy danych.
            create_chat_message(self, thread, user, msg): Metoda asynchroniczna tworząca nową wiadomość czatu w bazie danych.

    """
    async def websocket_connect(self, event):
        """
                Metoda wywoływana przy nawiązaniu połączenia WebSocket.

                Argumenty:
                    event (dict): Zdarzenie nawiązania połączenia WebSocket.

        """
        print('connected', event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        """
               Metoda wywoływana przy otrzymaniu wiadomości WebSocket.

               Argumenty:
                   event (dict): Zdarzenie otrzymania wiadomości WebSocket.

        """
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        send_by_id = received_data.get('send_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')

        if not msg:
            print('empty message')
            return False

        send_by_user = await self.get_user_object(send_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)

        if not send_by_user:
            print('Error:: send by user is incorrect')
        if not send_to_user:
            print('Error:: send to user is incorrect')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        await self.create_chat_message(thread_obj, send_by_user, msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']

        response = {
            'message': msg,
            'send_by': self_user.id,
            'thread_id': thread_id,
            'user_data': {
                'first_name': send_by_user.first_name,
                'last_name': send_by_user.last_name,
                'profile_picture': send_by_user.profile.profile_pic.url
            }
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )


    async def websocket_disconnect(self, event):
        """
                Metoda wywoływana przy rozłączeniu połączenia WebSocket.

                Argumenty:
                    event (dict): Zdarzenie rozłączenia połączenia WebSocket.

         """
        print('disconnect', event)

    async def chat_message(self, event):
        """
               Metoda wysyłająca wiadomość czatu do klienta WebSocket.

               Argumenty:
                   event (dict): Zdarzenie wysłania wiadomości czatu.

        """
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        """
                Metoda asynchroniczna pobierająca obiekt użytkownika z bazy danych.

                Argumenty:
                    user_id (int): Identyfikator użytkownika.

                Zwraca:
                    User: Obiekt użytkownika lub None, jeśli użytkownik nie istnieje.

        """
        try:
            user = User.objects.select_related('profile').get(id=user_id)
            return user
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_thread(self, thread_id):
        """
               Metoda asynchroniczna pobierająca obiekt wątku z bazy danych.

               Argumenty:
                   thread_id (int): Identyfikator wątku.

               Zwraca:
                   Thread: Obiekt wątku lub None, jeśli wątek nie istnieje.

        """
        q = Thread.objects.filter(id=thread_id)
        if q.exists():
            obj = q.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        """
               Metoda asynchroniczna tworząca nową wiadomość czatu w bazie danych.

               Argumenty:
                   thread (Thread): Obiekt wątku czatu.
                   user (User): Obiekt użytkownika wysyłającego wiadomość.
                   msg (str): Treść wiadomości.

        """
        ChatMessage.objects.create(thread=thread, user=user, message=msg)