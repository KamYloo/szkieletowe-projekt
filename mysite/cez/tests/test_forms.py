from datetime import datetime


from django.core.files.uploadedfile import SimpleUploadedFile
from cez.models import *
from cez.forms import *
from django.test import TestCase


class TestForms(TestCase):

    def test_submission_form_with_valid_data(self):
        file_data = {
            'file': SimpleUploadedFile("test_file.txt", b"file_content"),
        }
        form = SubmissionForm(data={}, files=file_data)
        self.assertTrue(form.is_valid())

    def test_submission_form_with_no_data(self):
        form = SubmissionForm(data={}, files={})
        self.assertFalse(form.is_valid())

    def test_course_form_with_valid_data(self):
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
        form = CourseForm(data={}, files={})
        self.assertFalse(form.is_valid())

    def test_access_key_form_valid_data(self):
        form = AccessKeyForm(data = {
            'access_key':'abc',
        })
        self.assertTrue(form.is_valid())

    def test_access_key_form_with_no_data(self):
        form = AccessKeyForm(data={})
        self.assertFalse(form.is_valid())

    def test_topic_update_form_with_valid_data(self):
        form_data = {
            'title': 'Updated Title',
            'content': 'updated content',
        }
        form = TopicUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_update_form_with_no_data(self):
        form = TopicUpdateForm(data={})
        self.assertFalse(form.is_valid())

    def test_assignment_form_with_valid_data(self):
        form_data = {
            'title': ' Assignment',
            'content': 'test assignment',
            'due_date': datetime.now(),
        }
        form = AssignmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_assignment_form_with_no_data(self):
        form = AssignmentForm(data={})
        self.assertFalse(form.is_valid())

    def test_assignment_update_form_with_valid_data(self):
        form_data = {
            'title': 'Updated Assignment',
            'content': ' updated assignment.',
            'due_date': datetime.now(),
        }
        form = AssignmentUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_assignment_update_form_with_no_data(self):
        form = AssignmentUpdateForm(data={})
        self.assertFalse(form.is_valid())

    def test_file_form_with_valid_data(self):
        file_content = b"Mock file content"
        mock_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")
        file_data = {
            'file':mock_file,
        }
        form = FileForm(data={}, files=file_data)
        self.assertTrue(form.is_valid())

    def test_file_form_with_no_data(self):
        form = FileForm(data={})
        self.assertFalse(form.is_valid())

    def test_course_file_form_with_valid_data(self):
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
        form = CourseFileForm(data={})
        self.assertFalse(form.is_valid())

    def test_rate_submission_form_with_valid_data(self):
        form_data = {
            'grade': 100,
            'comment': 'comment',
        }
        form = RateSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_rate_submission_form_with_no_data(self):
        form = RateSubmissionForm(data={})
        self.assertFalse(form.is_valid())

    def test_topic_form_with_valid_data(self):
        form_data = {
            'title': 'Title',
            'content': 'content',
        }
        form = TopicForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_topic_form_with_no_data(self):
        form = TopicForm(data={})
        self.assertFalse(form.is_valid())
