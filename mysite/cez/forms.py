from django import forms
from .models import Submission, Topic, Assignment, File, Course, Enrollment, RateSubmission, CourseFile

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

        widgets = {
            'file': forms.FileInput(attrs={'class': 'custom_file_input'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'semester', 'degree', 'access_key']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź nazwe kursu'}),
            'description': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
            'image': forms.FileInput(attrs={'class': 'custom_file_input'}),
            'semester': forms.Select(attrs={'class': 'custom_semester_select'}),
            'degree': forms.Select(attrs={'class': 'custom_degree_select'}),
            'access_key': forms.PasswordInput(attrs={'class': 'custom_access_key_input'}),
        }

class AccessKeyForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['access_key']
        widgets = {
            'access_key': forms.PasswordInput(attrs={'class': 'custom_access_key_input'}),
        }


class TopicUpdateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź tytuł'}),
            'content': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'due_date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź tytuł'}),
            'content': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
            'due_date': forms.DateInput(attrs={'class': 'custom_due_date_class', 'placeholder': 'Wprowadź termin'}),
        }

class AssignmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź tytuł'}),
            'content': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
            'due_date': forms.DateInput(attrs={'class': 'custom_due_date_class', 'placeholder': 'Wprowadź termin'}),
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

class CourseFileForm(forms.ModelForm):
    class Meta:
        model = CourseFile
        fields = ['name','file']

class RateSubmissionForm(forms.ModelForm):
    class Meta:
        model = RateSubmission
        fields = ['grade', 'comment']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'custom_grade_input', 'placeholder': 'Wprowadź ocene'}),
            'comment': forms.Textarea(attrs={'class': 'custom_comment_textarea', 'placeholder': 'Wprowadź komentarz'}),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title','content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź tytuł'}),
            'content': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
        }