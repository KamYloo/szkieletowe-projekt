from datetime import datetime


from django.core.files.uploadedfile import SimpleUploadedFile
from cez.models import *
from cez.forms import *
from django.test import TestCase


class TestForms(TestCase):
    """
       Klasa zawierająca testy dla formularzy aplikacji cez.

       Testy te sprawdzają poprawność działania formularzy.
    """

    def test_submission_form_with_valid_data(self):
        """
                Testuje formularz zgłoszenia z poprawnymi danymi.

                Sprawdza, czy formularz zgłoszenia jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        file_data = {
            'file': SimpleUploadedFile("test_file.txt", b"file_content"),
        }
        form = SubmissionForm(data={}, files=file_data)
        self.assertTrue(form.is_valid())

    def test_submission_form_with_no_data(self):
        """
            Testuje formularz zgłoszenia bez danych.

            Sprawdza, czy formularz zgłoszenia jest uznawany za niepoprawny,
            gdy nie podane są żadne dane.
        """

        form = SubmissionForm(data={}, files={})
        self.assertFalse(form.is_valid())

    def test_course_form_with_valid_data(self):
        """
                Testuje formularz kursu z poprawnymi danymi.

                Sprawdza, czy formularz kursu jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        degree = Degree.objects.create(degree="1")
        semester = Semester.objects.create(semester="1")
        with open('cez/tests/default_course.jpg', 'rb') as image_file:
            file_data = {
                'image': SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg"),
            }
        form_data = {
            'title': 'Test Course',
            'description': 'description',
            'semester': semester,
            'degree': degree,
            'access_key': 'test12',
        }
        form = CourseForm(data=form_data, files=file_data)
        # if not form.is_valid():
        #     print(form.errors)
        self.assertTrue(form.is_valid())

    def test_course_form_with_no_data(self):
        """
                Testuje formularz kursu bez danych.

                Sprawdza, czy formularz kursu jest uznawany za niepoprawny,
                gdy nie podane są żadne dane.
        """

        form = CourseForm(data={}, files={})
        self.assertFalse(form.is_valid())

    def test_access_key_form_valid_data(self):
        """
                Testuje formularz klucza dostępu z poprawnymi danymi.

                Sprawdza, czy formularz klucza dostępu jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        form = AccessKeyForm(data = {
            'access_key':'abc',
        })
        self.assertTrue(form.is_valid())

    def test_access_key_form_with_no_data(self):
        """
                Testuje formularz klucza dostępu bez danych.

                Sprawdza, czy formularz klucza dostępu jest uznawany za niepoprawny,
                gdy nie podane są żadne dane.
        """

        form = AccessKeyForm(data={})
        self.assertFalse(form.is_valid())

    def test_topic_update_form_with_valid_data(self):
        """
                Testuje formularz aktualizacji tematu z poprawnymi danymi.

                Sprawdza, czy formularz aktualizacji tematu jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        form_data = {
            'title': 'Updated Title',
            'content': 'updated content',
        }
        form = TopicUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_update_form_with_no_data(self):
        """
                Testuje formularz aktualizacji tematu bez danych.

                Sprawdza, czy formularz aktualizacji tematu jest uznawany za niepoprawny,
                gdy nie podane są żadne dane.
        """

        form = TopicUpdateForm(data={})
        self.assertFalse(form.is_valid())

    def test_assignment_form_with_valid_data(self):
        """
                Testuje formularz przypisania z poprawnymi danymi.

                Sprawdza, czy formularz przypisania jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        form_data = {
            'title': ' Assignment',
            'content': 'test assignment',
            'due_date': datetime.now(),
        }
        form = AssignmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_assignment_form_with_no_data(self):
        """
               Testuje formularz przypisania bez danych.

               Sprawdza, czy formularz przypisania jest uznawany za niepoprawny,
               gdy nie podane są żadne dane.
        """

        form = AssignmentForm(data={})
        self.assertFalse(form.is_valid())

    def test_assignment_update_form_with_valid_data(self):
        """
                Testuje formularz aktualizacji przypisania z poprawnymi danymi.

                Sprawdza, czy formularz aktualizacji przypisania jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        form_data = {
            'title': 'Updated Assignment',
            'content': ' updated assignment.',
            'due_date': datetime.now(),
        }
        form = AssignmentUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_assignment_update_form_with_no_data(self):
        """
                Testuje formularz aktualizacji przypisania bez danych.

                Sprawdza, czy formularz aktualizacji przypisania jest uznawany za niepoprawny,
                gdy nie podane są żadne dane.
        """

        form = AssignmentUpdateForm(data={})
        self.assertFalse(form.is_valid())

    def test_file_form_with_valid_data(self):
        """
                Testuje formularz pliku z poprawnymi danymi.

                Sprawdza, czy formularz pliku jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")
        file_data = {
            'file':mock_file,
        }
        form = FileForm(data={}, files=file_data)
        self.assertTrue(form.is_valid())

    def test_file_form_with_no_data(self):
        """
                Testuje formularz pliku bez danych.

                Sprawdza, czy formularz pliku jest uznawany za niepoprawny,
                gdy nie podane są żadne dane.
        """

        form = FileForm(data={})
        self.assertFalse(form.is_valid())

    def test_course_file_form_with_valid_data(self):
        """
                Testuje formularz pliku kursu z poprawnymi danymi.

                Sprawdza, czy formularz pliku kursu jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")
        file_data = {
            'file': mock_file,
        }
        form_data = {
                        'name': 'Test Course File',
        }
        form = CourseFileForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_course_file_form_with_no_data(self):
        """
                Testuje formularz pliku kursu bez danych.

                Sprawdza, czy formularz pliku kursu jest uznawany za niepoprawny,
                gdy nie podane są żadne dane.
        """

        form = CourseFileForm(data={})
        self.assertFalse(form.is_valid())

    def test_rate_submission_form_with_valid_data(self):
        """
                Testuje formularz oceny zgłoszenia z poprawnymi danymi.

                Sprawdza, czy formularz oceny zgłoszenia jest uznawany za poprawny,
                gdy podane są prawidłowe dane.
        """

        form_data = {
            'grade': 100,
            'comment': 'comment',
        }
        form = RateSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rate_submission_form_with_no_data(self):
        """
                Testuje formularz oceny zgłoszenia bez danych.

                Sprawdza, czy formularz oceny zgłoszenia jest uznawany za niepoprawny,
                gdy nie podane są żadne dane.
        """

        form = RateSubmissionForm(data={})
        self.assertFalse(form.is_valid())

    def test_topic_form_with_valid_data(self):
        """
               Testuje formularz tematu z poprawnymi danymi.

               Sprawdza, czy formularz tematu jest uznawany za poprawny,
               gdy podane są prawidłowe dane.
        """

        form_data = {
            'title': 'Title',
            'content': 'content',
        }
        form = TopicForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_form_with_no_data(self):
        """
                Testuje formularz tematu bez danych.

                Sprawdza, czy formularz tematu jest uznawany za niepoprawny,
                gdy nie podane są żadne dane.
        """

        form = TopicForm(data={})
        self.assertFalse(form.is_valid())
