from django.contrib import admin
from .models import Assignment, Submission, Topic, File
# Register your models here.
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Topic)
admin.site.register(File)

