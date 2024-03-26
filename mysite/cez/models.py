from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import shutil
import os
from PIL import Image

class Topic(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    files = models.ManyToManyField('File',blank=True)
    assignments = models.ManyToManyField('Assignment',blank=True)

    def __str__(self):
        return f"{self.title}"

class File(models.Model):
    file = models.FileField(upload_to='pdf_files/')

    def __str__(self):
        return f"{self.file.name}"

class Assignment(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    due_date = models.DateTimeField(default=datetime.now() + timedelta(weeks=1))
    topics = models.ManyToManyField('Topic', blank=True)

    def __str__(self):
        return f"{self.title}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='temp')

    # '''W dalszej części jeżeli będzie potrzeba to plik będzie zapisywany do folderu danego zadania'''
    # def save(self, *args, **kwargs ):
    #     super().save(*args, **kwargs)
    #     directory = f"/assignments/{self.pk}/"
    #     os.makedirs(directory, exist_ok=True)
    #     print(f"{self.file}")
    #     shutil.move(f"/{self.file}", directory)
    #     self.file = new_file
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Answer submitted by {self.student} to {self.assignment}"

class RateSubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    grade = models.FloatField(default=0)
    comment = models.CharField(max_length=1024)


class Semester(models.Model):
    semester = models.CharField(max_length=50)
    def __str__(self):
        return self.semester

class Degree(models.Model):
    degree = models.CharField(max_length=50)
    def __str__(self):
        return self.degree
class Course(models.Model):
   teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
   topics = models.ManyToManyField(Topic, blank=True)
   title = models.CharField(max_length=100)
   description = models.TextField()
   semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
   degree = models.ForeignKey(Degree, on_delete=models.CASCADE, default=1)
   image = models.ImageField(upload_to='course_images/', blank=True, null=True, default="course_images/default_course.jpg")
   access_key = models.CharField(max_length=50, unique=True)
   def __str__(self):
       return self.title

   def save(self):
       super().save()

       img = Image.open(self.image.path)

       if img.height > 612 or img.width > 408:
           output_size = (612, 408)
           img.thumbnail(output_size)
           img.save(self.image.path)

class Student(models.Model):
   student = models.OneToOneField(User, on_delete=models.CASCADE)
   courses = models.ManyToManyField(Course, related_name='students')


class Enrollment(models.Model):
   student = models.ForeignKey(User, on_delete=models.CASCADE)
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   access_key = models.CharField(max_length=50)
   joined_at = models.DateTimeField(auto_now_add=True)




