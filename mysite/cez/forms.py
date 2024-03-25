from django import forms
from .models import Submission, Topic, Assignment, File

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

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