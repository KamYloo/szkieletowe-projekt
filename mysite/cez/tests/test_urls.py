# from django.test import SimpleTestCase
# from django.urls import resolve, reverse
# from cez.views import *
#
#
# class TestUrls(SimpleTestCase):
#
#     def test_index_url_is_resolved(self):
#         url = reverse('index')
#         self.assertEquals(resolve(url).func, index)
#
#     def test_enroll_url_is_resolved(self):
#         url = reverse('enroll_to_course', args=[1])
#         self.assertEquals(resolve(url).func, enroll_to_course)
#
#     def test_course_url_is_resolved(self):
#         url = reverse('courses')
#         self.assertEquals(resolve(url).func, courses)
#
#     def test_create_course_url_is_resolved(self):
#         url = reverse('create-course')
#         self.assertEquals(resolve(url).func, create_course)
#
#     def test_course_delete_url_is_resolved(self):
#         url = reverse('delete_course', args=[1])
#         self.assertEquals(resolve(url).func, delete_course)
#
#     def test_course_detail_url_is_resolved(self):
#         url = reverse('course_detail', args=[1])
#         self.assertEquals(resolve(url).func, course_detail)
#
#     def test_add_topic_url_is_resolved(self):
#         url = reverse('add-topic', args=[1])
#         self.assertEquals(resolve(url).func, add_topic)
#
#     def test_update_topic_url_is_resolved(self):
#         url = reverse('topic-update', args=[1, 1])
#         self.assertEquals(resolve(url).func, update_topic)
#
#     def test_delete_topic_url_is_resolved(self):
#         url = reverse('topic-delete', args=[1, 1])
#         self.assertEquals(resolve(url).func, delete_topic)
#
#     def test_create_assignment_url_is_resolved(self):
#         url = reverse('create-assignments', args=[1, 1])
#         self.assertEquals(resolve(url).func, create_assignments)
#
#     def test_update_assignment_url_is_resolved(self):
#         url = reverse('assignment-update', args=[1, 1])
#         self.assertEquals(resolve(url).func, update_assignment)
#
#     def test_remove_assignment_url_is_resolved(self):
#         url = reverse('assignment-remove', args=[1, 1])
#         self.assertEquals(resolve(url).func, remove_assignment)
#
#     def test_rate_assignment_url_is_resolved(self):
#         url = reverse('assignment-rate', args=[1, 1])
#         self.assertEquals(resolve(url).func, rate_assignment)
#
#     def test_rate_users_assignment_url_is_resolved(self):
#         url = reverse('assignment-rate-by-user', args=[1, 1, 1])
#         self.assertEquals(resolve(url).func, rate_users_assignment)
#
#     def test_add_file_url_is_resolved(self):
#         url = reverse('add-file', args=[1, 1])
#         self.assertEquals(resolve(url).func, add_file)
#
#     def test_delete_file_url_is_resolved(self):
#         url = reverse('delete-file', args=[1, 1])
#         self.assertEquals(resolve(url).func, delete_file)
#
#     def test_assignment_submit_url_is_resolved(self):
#         url = reverse('assignment-submit', args=[1])
#         self.assertEquals(resolve(url).func, submit_assignment)
