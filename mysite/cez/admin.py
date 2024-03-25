from django.contrib import admin
from .models import Assignment,Submission, Degree , Semester, Course, Student, Enrollment
from .models import Assignment, Submission, Topic, File
# Register your models here.
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Degree)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Topic)
admin.site.register(File)

