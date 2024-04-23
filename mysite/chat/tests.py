from django.test import TestCase, SimpleTestCase, RequestFactory, Client
from django.contrib.auth.models import User
from .models import Thread, ChatMessage
from django.urls import reverse, resolve
from .views import chat, create_thread, delete_thread, search_thread
from django.contrib.messages.storage.fallback import FallbackStorage
import json

class ThreadModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password')

    def test_thread_creation(self):
        thread = Thread.objects.create(first_person=self.user1, second_person=self.user2)
        self.assertIsInstance(thread, Thread)
        self.assertEqual(thread.first_person, self.user1)
        self.assertEqual(thread.second_person, self.user2)

class ChatMessageModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password')
        self.thread = Thread.objects.create(first_person=self.user1, second_person=self.user2)

    def test_chat_message_creation(self):
        message = ChatMessage.objects.create(thread=self.thread, user=self.user1, message='Test message')
        self.assertIsInstance(message, ChatMessage)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.user, self.user1)
        self.assertEqual(message.message, 'Test message')


class TestUrls(SimpleTestCase):

    def test_chat_url_resolves(self):
        url = reverse('chat')
        self.assertEqual(resolve(url).func, chat)

    def test_search_thread_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, search_thread)

    def test_create_thread_url_resolves(self):
        url = reverse('create_thread_chat', args=[1])
        self.assertEqual(resolve(url).func, create_thread)

    def test_delete_thread_url_resolves(self):
        url = reverse('delete_thread', args=[1]) 
        self.assertEqual(resolve(url).func, delete_thread)


class TestChatViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password', first_name='John', last_name='Doe')
        self.user2 = User.objects.create_user(username='user2', password='password', first_name='Jane', last_name='Doe')

    def test_chat_view(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(reverse('chat'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat.html')

    def test_create_thread_view(self):
        self.client.login(username='user1', password='password')
        response = self.client.post(reverse('create_thread_chat', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, 302)

        thread_exists = Thread.objects.filter(first_person=self.user1, second_person=self.user2).exists()
        self.assertTrue(thread_exists)

    def test_delete_thread_view(self):
        thread = Thread.objects.create(first_person=self.user1, second_person=self.user2)
        self.client.login(username='user1', password='password')
        response = self.client.post(reverse('delete_thread', kwargs={'thread_id': thread.pk}))
        self.assertEqual(response.status_code, 302)

        # Check if the thread was deleted
        thread_exists = Thread.objects.filter(pk=thread.pk).exists()
        self.assertFalse(thread_exists)

class SearchThreadTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_search_thread_ajax(self):
        self.client.login(username='testuser', password='password123')

        # Tworzenie zapytania ajax
        url = reverse('search')
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Sprawdzenie odpowiedzi
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_search_thread_results(self):
        self.client.login(username='testuser', password='password123')
        User.objects.create(username='test1', first_name='John', last_name='Doe')
        User.objects.create(username='test2', first_name='Jane', last_name='Doe')

        # Zapytanie POST z danymi
        url = reverse('search')
        response = self.client.post(url, {'users': 'Doe'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Sprawdzenie odpowiedzi
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['first_name'], 'John')
        self.assertEqual(data['data'][1]['first_name'], 'Jane')

    def test_search_thread_no_results(self):
        self.client.login(username='testuser', password='password123')

        # Zapytanie POST z danymi niezwracającymi wyników
        url = reverse('search')
        response = self.client.post(url, {'users': 'NonExistingUser'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Sprawdzenie odpowiedzi
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['data'], "No Users Found...")

    def test_search_thread_no_ajax(self):
        self.client.login(username='testuser', password='password123')

        # Zapytanie bez nagłówka XMLHttpRequest
        url = reverse('search')
        response = self.client.post(url)

        # Sprawdzenie odpowiedzi
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.content.decode('utf-8'), '{}')