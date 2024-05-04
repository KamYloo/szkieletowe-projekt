from django.test import SimpleTestCase
from django.urls import resolve, reverse
from cez.views import *


class TestUrls(SimpleTestCase):
    """
        Klasa zawierająca testy rozwiązywania adresów URL aplikacji cez.

        Testy te sprawdzają, czy adresy URL prowadzą do odpowiednich widoków.
    """

    def test_index_url_is_resolved(self):
        """
                Testuje, czy adres URL dla strony głównej jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'index'.
        """

        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_enroll_url_is_resolved(self):
        """
                Testuje, czy adres URL dla zapisu na kurs jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'enroll_to_course'.
        """

        url = reverse('enroll_to_course', args=[1])
        self.assertEquals(resolve(url).func, enroll_to_course)

    def test_course_url_is_resolved(self):
        """
                Testuje, czy adres URL dla listy kursów jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'courses'.
        """

        url = reverse('courses')
        self.assertEquals(resolve(url).func, courses)

    def test_create_course_url_is_resolved(self):
        """
                Testuje, czy adres URL dla tworzenia kursu jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'create_course'.
        """

        url = reverse('create-course')
        self.assertEquals(resolve(url).func, create_course)

    def test_course_delete_url_is_resolved(self):
        """
               Testuje, czy adres URL dla usuwania kursu jest rozwiązywany poprawnie.

               Sprawdza, czy adres URL prowadzi do widoku 'delete_course'.
        """

        url = reverse('delete_course', args=[1])
        self.assertEquals(resolve(url).func, delete_course)

    def test_course_detail_url_is_resolved(self):
        """
                Testuje, czy adres URL dla szczegółów kursu jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'course_detail'.
        """

        url = reverse('course_detail', args=[1])
        self.assertEquals(resolve(url).func, course_detail)

    def test_add_topic_url_is_resolved(self):
        """
                Testuje, czy adres URL dla dodawania tematu jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'add_topic'.
        """

        url = reverse('add-topic', args=[1])
        self.assertEquals(resolve(url).func, add_topic)

    def test_update_topic_url_is_resolved(self):
        """
                Testuje, czy adres URL dla aktualizacji tematu jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'update_topic'.
        """

        url = reverse('topic-update', args=[1, 1])
        self.assertEquals(resolve(url).func, update_topic)

    def test_delete_topic_url_is_resolved(self):
        """
                Testuje, czy adres URL dla usuwania tematu jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'delete_topic'.
        """

        url = reverse('topic-delete', args=[1, 1])
        self.assertEquals(resolve(url).func, delete_topic)

    def test_create_assignment_url_is_resolved(self):
        """
                Testuje, czy adres URL dla tworzenia przypisania jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'create_assignments'.
        """

        url = reverse('create-assignments', args=[1, 1])
        self.assertEquals(resolve(url).func, create_assignments)

    def test_update_assignment_url_is_resolved(self):
        """
                Testuje, czy adres URL dla aktualizacji przypisania jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'update_assignment'.
        """

        url = reverse('assignment-update', args=[1, 1])
        self.assertEquals(resolve(url).func, update_assignment)

    def test_remove_assignment_url_is_resolved(self):
        """
               Testuje, czy adres URL dla usuwania przypisania jest rozwiązywany poprawnie.

               Sprawdza, czy adres URL prowadzi do widoku 'remove_assignment'.
        """

        url = reverse('assignment-remove', args=[1, 1])
        self.assertEquals(resolve(url).func, remove_assignment)

    def test_rate_assignment_url_is_resolved(self):
        """
                Testuje, czy adres URL dla oceny przypisania jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'rate_assignment'.
        """

        url = reverse('assignment-rate', args=[1, 1])
        self.assertEquals(resolve(url).func, rate_assignment)

    def test_rate_users_assignment_url_is_resolved(self):
        """
                Testuje, czy adres URL dla oceny przypisania przez użytkownika jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'rate_users_assignment'.
        """

        url = reverse('assignment-rate-by-user', args=[1, 1, 1])
        self.assertEquals(resolve(url).func, rate_users_assignment)

    def test_add_file_url_is_resolved(self):
        """
                Testuje, czy adres URL dla dodawania pliku jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'add_file'.
        """

        url = reverse('add-file', args=[1, 1])
        self.assertEquals(resolve(url).func, add_file)

    def test_delete_file_url_is_resolved(self):
        """
               Testuje, czy adres URL dla usuwania pliku jest rozwiązywany poprawnie.

               Sprawdza, czy adres URL prowadzi do widoku 'delete_file'.
        """

        url = reverse('delete-file', args=[1, 1])
        self.assertEquals(resolve(url).func, delete_file)

    def test_assignment_submit_url_is_resolved(self):
        """
                Testuje, czy adres URL dla zgłaszania przypisania jest rozwiązywany poprawnie.

                Sprawdza, czy adres URL prowadzi do widoku 'submit_assignment'.
        """

        url = reverse('assignment-submit', args=[1])
        self.assertEquals(resolve(url).func, submit_assignment)
