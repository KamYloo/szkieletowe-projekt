from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from cez.views import *
from cez.models import *

import json

class TestViews(TestCase):
    """
        Klasa zawierająca testy widoków aplikacji CEZ.

        Testy te sprawdzają poprawność działania poszczególnych widoków.
    """

    def setUp(self):
        """
                Metoda konfiguracyjna, inicjalizująca obiekty niezbędne do przeprowadzenia testów.
        """

        self.client = Client()
        self.user = User.objects.create_user(username='test',
                                             password='12345')
        self.user_non_teacher = User.objects.create_user(username='test2',
                                             password='12345')
        self.group = Group.objects.create(name='Nauczyciel')
        self.user.groups.add(self.group)
        self.degree = Degree.objects.create(degree="1")
        self.semester = Semester.objects.create(semester="1")
        self.course = Course.objects.create(teacher=self.user.profile, title="Math",
                                            description="test",
                                            access_key="abc",
                                            degree=self.degree,
                                            semester=self.semester)
        self.topic = Topic.objects.create(title='Test Topic',
                                          content="Test desc")
        self.course.topics.add(self.topic)
        self.course_id = self.course.pk
        self.topic_id = self.topic.pk
        self.assignment = Assignment.objects.create(title='Math Assignment',
                                                    content='Test Description',
                                                    due_date=datetime.now())
        self.topic.assignments.add(self.assignment)
        self.assignment.topics.add(self.topic_id)
        self.assignment_id = self.assignment.pk

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        self.coursefile = CourseFile.objects.create(name="test file 80", file=mock_file)
        self.coursefile_id = self.coursefile.pk


    def test_index_GET(self):
        """
                Testuje widok strony głównej.

                Sprawdza, czy widok strony głównej jest dostępny i używa odpowiedniego szablonu.
        """

        url = reverse('index')
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/index.html')

    def test_courses_GET(self):
        """
                Testuje widok listy kursów.

                Sprawdza, czy widok listy kursów jest dostępny i używa odpowiedniego szablonu.
        """

        url = reverse('courses')
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/courses.html')

    def test_create_assignment_view_GET(self):
        """
                Testuje widok tworzenia zadania (GET) dla nauczyciela.

                Sprawdza, czy widok tworzenia zadania dla nauczyciela jest dostępny i używa odpowiedniego szablonu.
        """

        self.client.login(username='test', password='12345')
        url = reverse('create-assignments', args=[self.course_id, self.topic_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/create_assignment.html')
        self.client.logout()

    def test_create_assignment_view_POST_with_valid_data(self):
        """
               Testuje tworzenie zadania (POST) z poprawnymi danymi przez nauczyciela.

               Sprawdza, czy zadanie jest tworzone poprawnie po przesłaniu poprawnych danych przez nauczyciela.
        """

        self.client.login(username='test', password='12345')
        url = reverse('create-assignments', args=[self.course_id, self.topic_id])
        data = {'title': 'Math Assignment',
                'content': 'Test Description',
                'due_date': datetime.now(),
                'topics': self.topic_id}
        response = self.client.post(url, data, follow=True)
        self.assertTrue(Assignment.objects.filter(title='Math Assignment').exists())
        self.assertTemplateUsed(response, 'cez/course_detail.html')

    def test_create_assignment_view_POST_with_out_data(self):
        """
                Testuje tworzenie zadania (POST) bez danych przez nauczyciela.

                Sprawdza, czy nauczyciel nie może utworzyć zadania, gdy dane nie są przekazane.
        """

        self.client.login(username='test', password='12345')
        url = reverse('create-assignments', args=[self.course_id, self.topic_id])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/create_assignment.html')
        self.client.logout()

    def test_create_assignment_view_POST_with_valid_data_by_non_teacher(self):
        """
                Testuje tworzenie zadania (POST) przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może utworzyć zadania.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('create-assignments', args=[self.course_id, self.topic_id])
        data = {'title': 'Math Assignment',
                'content': 'Test Description',
                'due_date': datetime.now(),
                'topics': self.topic_id}
        response = self.client.post(url, data, follow = True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_submit_assignment_POST(self):
        """
                Testuje przesyłanie rozwiązania zadania (POST) przez studenta.

                Sprawdza, czy student może przesłać rozwiązanie zadania i czy zostanie ono zapisane w systemie.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('assignment-submit', args=[self.assignment_id])

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        data = {
            'assignment_id': self.assignment_id,
            'student': self.user_non_teacher,
            'submission_date':  datetime.now(),
            'file': mock_file,
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Submission.objects.filter(assignment_id=self.assignment_id, student=self.user_non_teacher).exists())
        self.assertTemplateUsed(response, 'cez/submit_assignment.html')
        self.client.logout()

    def test_submit_assignment_GET(self):
        """
                Testuje dostęp do formularza przesyłania rozwiązania zadania (GET) przez studenta.

                Sprawdza, czy student może uzyskać dostęp do formularza przesyłania rozwiązania zadania.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('assignment-submit', args=[self.assignment_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/submit_assignment.html')
        self.client.logout()

    def test_create_course_GET(self):
        """
                Testuje dostęp do formularza tworzenia kursu (GET) przez nauczyciela.

                Sprawdza, czy nauczyciel może uzyskać dostęp do formularza tworzenia nowego kursu.
        """

        self.client.login(username='test', password='12345')
        url = reverse('create-course')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/create_course_form.html')
        self.client.logout()

    def test_create_course_GET_non_teacher(self):
        """
                Testuje dostęp do formularza tworzenia kursu (GET) przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może uzyskać dostępu do formularza tworzenia kursu.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('create-course')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.client.logout()

    def test_create_course_POST(self):
        """
                Testuje tworzenie nowego kursu (POST) przez nauczyciela.

                Sprawdza, czy nauczyciel może utworzyć nowy kurs i czy zostanie on zapisany w systemie.
        """

        self.client.login(username='test', password='12345')
        url = reverse('create-course')
        data = {
            'title': 'Discrete Math',
            'description': 'Test Description',
            'access_key': 'testkey',
            'degree': self.degree.pk,
            'semester': self.semester.pk,
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/courses.html')
        self.assertTrue(Course.objects.filter(teacher=self.user.profile, title = 'Discrete Math').exists())
        self.client.logout()

    def test_create_course_POST_non_teacher(self):
        """
                Testuje tworzenie nowego kursu (POST) przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może utworzyć nowego kursu.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('create-course')
        data = {
            'title': 'Discrete Math',
            'description': 'Test Description',
            'access_key': 'testkey',
            'degree': self.degree.pk,
            'semester': self.semester.pk,
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_delete_course_teacher(self):
        """
                Testuje usuwanie kursu przez nauczyciela.

                Sprawdza, czy nauczyciel może usunąć kurs z systemu.
        """

        self.client.login(username='test', password='12345')
        course2 = Course.objects.create(teacher=self.user.profile,
                                        title="PEiE",
                                        description="test",
                                        access_key="abc",
                                        degree=self.degree,
                                        semester=self.semester)
        url = reverse('delete_course', args=[course2.pk])
        response = self.client.delete(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cez/courses.html')
        self.client.logout()

    def test_delete_course_teacher_non_teacher(self):
        """
                Testuje usuwanie kursu przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może usunąć kursu z systemu.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('delete_course', args=[self.course_id])
        response = self.client.delete(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_update_assignment_POST_teacher(self):
        """
               Testuje aktualizację zadania (POST) przez nauczyciela.

               Sprawdza, czy nauczyciel może zaktualizować istniejące zadanie.
        """

        self.client.login(username='test', password='12345')
        url = reverse('assignment-update', args=[self.course_id, self.assignment_id])
        data = {
            'title': 'Discrete Math Assignment',
            'content': 'Test Description',
            'due_date': datetime.now(),
            'topics': self.topic_id
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/course_detail.html')
        self.assertTrue(Assignment.objects.filter(title='Discrete Math Assignment').exists())
        self.client.logout()

    def test_update_assignment_POST_non_teacher(self):
        """
                Testuje aktualizację zadania (POST) przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może zaktualizować zadania.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('assignment-update', args=[self.course_id, self.assignment_id])
        data = {
            'title': 'Discrete Math Assignment',
            'content': 'Test Description',
            'due_date': datetime.now(),
            'topics': self.topic_id
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_remove_assignment_POST_non_teacher(self):
        """
                Testuje usuwanie zadania (POST) przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może usunąć zadania.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('assignment-remove', args=[self.course_id, self.assignment_id])
        response = self.client.delete(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_remove_assignment_POST_teacher(self):
        """
                Testuje usuwanie zadania (POST) przez nauczyciela.

                Sprawdza, czy nauczyciel może usunąć zadanie.
        """

        self.client.login(username='test', password='12345')
        url = reverse('assignment-remove', args=[self.course_id, self.assignment_id])
        response = self.client.delete(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/course_detail.html')
        self.client.logout()

    def test_enroll_to_course(self):
        """
                Testuje zapisanie się na kurs przez studenta.

                Sprawdza, czy student może zapisać się na kurs, korzystając z klucza dostępu.
        """

        self.client.login(username='test2', password='12345')
        course2 = Course.objects.create(teacher=self.user.profile,
                                        title="PEiE",
                                        description="test",
                                        access_key="abc",
                                        degree=self.degree,
                                        semester=self.semester)
        url = reverse('enroll_to_course', args=[course2.pk])
        response = self.client.post(url, {'access_key':"abc"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Enrollment.objects.filter(course=course2, student=self.user_non_teacher).exists())
        self.client.logout()

    def test_enroll_to_course_invalid_password(self):
        """
                Testuje zapisanie się na kurs przez studenta z nieprawidłowym kluczem dostępu.

                Sprawdza, czy student nie może zapisać się na kurs, gdy poda nieprawidłowy klucz dostępu.
        """

        self.client.login(username='test2', password='12345')
        course3 = Course.objects.create(teacher=self.user.profile,
                                        title="PEiE2",
                                        description="test",
                                        access_key="abc",
                                        degree=self.degree,
                                        semester=self.semester)
        url = reverse('enroll_to_course', args=[course3.pk])
        response = self.client.post(url, {'access_key': "213"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Enrollment.objects.filter(course=course3, student=self.user_non_teacher).exists())
        self.client.logout()

    def test_update_topic_GET_invalid_topic(self):
        """
                Testuje dostęp do aktualizacji tematu (GET) dla nieistniejącego tematu.

                Sprawdza, czy użytkownik może uzyskać dostęp do formularza aktualizacji tematu,
                nawet jeśli temat nie istnieje.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('topic-update', args=[self.course_id, 9])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_update_topic_GET_valid_topic(self):
        """
                Testuje dostęp do aktualizacji tematu (GET) dla istniejącego tematu.

                Sprawdza, czy użytkownik może uzyskać dostęp do formularza aktualizacji istniejącego tematu.
        """

        self.client.login(username='test', password='12345')
        url = reverse('topic-update', args=[self.course_id, self.topic_id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/topic_update.html')
        self.client.logout()

    def test_update_topic_POST_none_teacher(self):
        """
                Testuje aktualizację tematu (POST) przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może aktualizować tematu.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('topic-update', args=[self.course_id, self.topic_id])

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        file = CourseFile.objects.create(name="test", file=mock_file)

        data = {
            'title':'Obliczanie rezystancji',
            'content':'Mr Green cie nauczy',
            'files': file,
            'assignments': self.assignment
        }

        response = self.client.post(url, data,follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Topic.objects.filter(title='Obliczanie rezystancji').exists())
        self.client.logout()

    def test_update_topic_POST_teacher(self):
        """
                Testuje aktualizację tematu (POST) przez nauczyciela.

                Sprawdza, czy nauczyciel może zaktualizować istniejący temat.
        """

        self.client.login(username='test', password='12345')
        url = reverse('topic-update', args=[self.course_id, self.topic_id])

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        file = CourseFile.objects.create(name="test", file=mock_file)

        data = {
            'title': 'Obliczanie rezystancji',
            'content': 'Mr Green cie nauczy',
            'files': file,
            'assignments': self.assignment
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Topic.objects.filter(title='Obliczanie rezystancji').exists())
        self.client.logout()

    def test_add_topic_GET_none_teacher(self):
        """
                Testuje dostęp do formularza dodawania tematu (GET) dla użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może uzyskać dostępu do formularza dodawania tematu.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('add-topic', args=[self.course_id])

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_add_topic_GET_teacher(self):
        """
                Testuje dostęp do formularza dodawania tematu (GET) dla nauczyciela.

                Sprawdza, czy nauczyciel może uzyskać dostęp do formularza dodawania tematu.
        """

        self.client.login(username='test', password='12345')
        url = reverse('add-topic', args=[self.course_id])

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/add_topic.html')
        self.client.logout()

    def test_add_topic_POST_none_teacher(self):
        """
                Testuje dodawanie tematu (POST) przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może dodać nowego tematu.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('add-topic', args=[self.course_id])

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        file = CourseFile.objects.create(name="test", file=mock_file)

        data = {
            'title': 'Obliczanie superpozycji',
            'content': 'Mr Green cie nauczy tego tez',
            'files': file,
            'assignments': self.assignment
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Topic.objects.filter(title='Obliczanie superpozycji').exists())
        self.client.logout()

    def test_add_topic_POST_teacher(self):
        """
                Testuje dodawanie tematu (POST) przez nauczyciela.

                Sprawdza, czy nauczyciel może dodać nowy temat.
        """

        self.client.login(username='test', password='12345')
        url = reverse('add-topic', args=[self.course_id])

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        file = CourseFile.objects.create(name="test", file=mock_file)

        data = {
            'title': 'Obliczanie superpozycji',
            'content': 'Mr Green cie nauczy tego tez',
            'files': file,
            'assignments': self.assignment
        }

        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Topic.objects.filter(title='Obliczanie superpozycji').exists())
        self.client.logout()

    def test_course_detail_get(self):
        """
                Testuje dostęp do szczegółów kursu (GET) przez studenta.

                Sprawdza, czy student może uzyskać dostęp do szczegółów kursu.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('course_detail', args=[self.course_id])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/course_detail.html')
        self.client.logout()

    def test_rate_assignment_get_none_teacher(self):
        """
               Testuje dostęp do oceny zadania (GET) przez użytkownika nie będącego nauczycielem.

               Sprawdza, czy użytkownik nie będący nauczycielem nie może uzyskać dostępu do oceny zadania.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('assignment-rate', args=[self.course_id, self.assignment_id])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 404)
        self.client.logout()

    def test_rate_assignment_get_teacher(self):
        """
               Testuje dostęp do oceny zadania (GET) przez nauczyciela.

               Sprawdza, czy nauczyciel może uzyskać dostęp do oceny zadania.
        """

        self.client.login(username='test', password='12345')
        url = reverse('assignment-rate', args=[self.course_id, self.assignment_id])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'cez/rate_assignment.html')
        self.client.logout()

    def test_delete_topic_none_teacher(self):
        """
               Testuje usuwanie tematu przez użytkownika nie będącego nauczycielem.

               Sprawdza, czy użytkownik nie będący nauczycielem nie może usunąć tematu.
        """

        self.client.login(username='test2', password='12345')
        url = reverse('topic-delete', args=[self.course_id, self.topic_id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Topic.objects.filter(pk=self.topic_id).exists())
        self.client.logout()


    def test_delete_topic_teacher(self):
        """
                Testuje usuwanie tematu przez nauczyciela.

                Sprawdza, czy nauczyciel może usunąć temat.
        """

        self.client.login(username='test', password='12345')
        url = reverse('topic-delete', args=[self.course_id, self.topic_id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.filter(pk=self.topic_id).exists())
        self.client.logout()

    def test_add_coursefilee_none_teacher(self):
        """
                Testuje dodawanie pliku do kursu przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może dodać pliku do kursu.
        """

        self.client.login(username='test2', password='12345')

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        data = {
            'name': 'test file 808',
            'file': mock_file
        }

        url = reverse('add-file', args=[self.course_id, self.topic_id])
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(CourseFile.objects.filter(name="test file 808").exists())
        self.client.logout()

    def test_add_coursefile_teacher(self):
        """
                Testuje dodawanie pliku do kursu przez nauczyciela.

                Sprawdza, czy nauczyciel może dodać plik do kursu.
        """

        self.client.login(username='test', password='12345')

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        data = {
            'name': 'test file 808',
            'file': mock_file
        }

        url = reverse('add-file', args=[self.course_id, self.topic_id])
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CourseFile.objects.filter(name="test file 808").exists())
        self.client.logout()

    def test_delete_coursefile_none_teacher(self):
        """
                Testuje usuwanie pliku z kursu przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może usunąć pliku z kursu.
        """

        self.client.login(username='test2', password='12345')

        url = reverse('delete-file', args=[self.course_id, self.coursefile_id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(CourseFile.objects.filter(pk=self.coursefile_id).exists())
        self.client.logout()

    def test_delete_coursefile_teacher(self):
        """
                Testuje usuwanie pliku z kursu przez nauczyciela.

                Sprawdza, czy nauczyciel może usunąć plik z kursu.
        """

        self.client.login(username='test', password='12345')
        self.assertTrue(CourseFile.objects.filter(pk=self.coursefile_id).exists())
        url = reverse('delete-file', args=[self.course_id, self.coursefile_id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CourseFile.objects.filter(pk=self.coursefile_id).exists())
        self.client.logout()

    def test_rate_POST_none_teacher(self):
        """
                Testuje ocenianie rozwiązania zadania przez użytkownika nie będącego nauczycielem.

                Sprawdza, czy użytkownik nie będący nauczycielem nie może ocenić rozwiązania zadania.
        """

        self.client.login(username='test2', password='12345')
        submission = Submission.objects.create(assignment_id=self.assignment_id, student=self.user_non_teacher)
        url = reverse('assignment-rate-by-user', args=[self.course_id, self.assignment_id, submission.pk])
        data = {
            'assignment': self.assignment_id,
            'teacher': self.user.profile,
            'student': self.user_non_teacher,
            'grade': '100',
            'comment': 'lkjh'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(RateSubmission.objects.filter(comment="lkjh").exists())
        self.client.logout()

    def test_rate_POST_teacher(self):
        """
               Testuje ocenianie rozwiązania zadania przez nauczyciela.

               Sprawdza, czy nauczyciel może ocenić rozwiązanie zadania.
        """

        self.client.login(username='test', password='12345')
        submission = Submission.objects.create(assignment_id=self.assignment_id, student=self.user_non_teacher)
        self.client.login(username='test', password='12345')
        url = reverse('assignment-rate-by-user', args=[self.course_id, self.assignment_id, submission.pk])
        data = {
            'assignment': self.assignment_id,
            'teacher': self.user.profile,
            'student': self.user_non_teacher,
            'grade': '100',
            'comment': 'lkjh'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(RateSubmission.objects.filter(comment="lkjh").exists())
        self.client.logout()

