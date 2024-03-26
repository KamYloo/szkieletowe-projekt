from django import forms
from .models import Submission, Topic, Assignment, File, Course, Enrollment, RateSubmission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'semester', 'degree', 'access_key']

class AccessKeyForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['access_key']


class TopicUpdateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'due_date']

class AssignmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'due_date']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

class RateSubmissionForm(forms.ModelForm):
    class Meta:
        model = RateSubmission
        fields = ['grade', 'comment']