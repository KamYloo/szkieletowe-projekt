from django import forms
from .models import Submission, Topic, Assignment, File, Course, Enrollment, RateSubmission, CourseFile

class SubmissionForm(forms.ModelForm):
    """
       Formularz do przesyłania zgłoszeń zadań.

       Pola:
           file (FileField): Pole do wyboru pliku zgłoszenia.

    """

    class Meta:
        model = Submission
        fields = ['file']

        widgets = {
            'file': forms.FileInput(attrs={'class': 'custom_file_input'}),
        }

class CourseForm(forms.ModelForm):
    """
       Formularz do tworzenia kursu.

       Pola:
           title (CharField): Pole do wprowadzenia tytułu kursu.
           description (TextField): Pole do wprowadzenia opisu kursu.
           image (FileField): Pole do wyboru obrazu reprezentującego kurs.
           semester (ForeignKey): Pole do wyboru semestru, do którego przypisany jest kurs.
           degree (ForeignKey): Pole do wyboru stopnia naukowego, do którego przypisany jest kurs.
           access_key (CharField): Pole do wprowadzenia klucza dostępu do kursu.

    """

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
    """
        Formularz do wprowadzenia klucza dostępu.

        Pola:
            access_key (CharField): Pole do wprowadzenia klucza dostępu.

    """

    class Meta:
        model = Enrollment
        fields = ['access_key']
        widgets = {
            'access_key': forms.PasswordInput(attrs={'class': 'custom_access_key_input'}),
        }


class TopicUpdateForm(forms.ModelForm):
    """
        Formularz do aktualizacji tematu.

        Pola:
            title (CharField): Pole do wprowadzenia tytułu tematu.
            content (TextField): Pole do wprowadzenia treści tematu.

    """

    class Meta:
        model = Topic
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź tytuł'}),
            'content': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
        }

class AssignmentForm(forms.ModelForm):
    """
        Formularz do tworzenia nowego zadania.

        Pola:
            title (CharField): Pole do wprowadzenia tytułu zadania.
            content (TextField): Pole do wprowadzenia treści zadania.
            due_date (DateField): Pole do wprowadzenia terminu wykonania zadania.

    """

    class Meta:
        model = Assignment
        fields = ['title', 'content', 'due_date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź tytuł'}),
            'content': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
            'due_date': forms.DateInput(attrs={'class': 'custom_due_date_class', 'placeholder': 'Wprowadź termin'}),
        }

class AssignmentUpdateForm(forms.ModelForm):
    """
        Formularz do aktualizacji istniejącego zadania.

        Pola:
            title (CharField): Pole do wprowadzenia tytułu zadania.
            content (TextField): Pole do wprowadzenia treści zadania.
            due_date (DateField): Pole do wprowadzenia terminu wykonania zadania.

    """

    class Meta:
        model = Assignment
        fields = ['title', 'content', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź tytuł'}),
            'content': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
            'due_date': forms.DateInput(attrs={'class': 'custom_due_date_class', 'placeholder': 'Wprowadź termin'}),
        }

class FileForm(forms.ModelForm):
    """
       Formularz do przesyłania pliku.

       Pola:
           file (FileField): Pole do wyboru pliku.

    """

    class Meta:
        model = File
        fields = ['file']

class CourseFileForm(forms.ModelForm):
    """
        Formularz do przesyłania pliku kursowego.

        Pola:
            name (CharField): Pole do wprowadzenia nazwy pliku.
            file (FileField): Pole do wyboru pliku.

    """

    class Meta:
        model = CourseFile
        fields = ['name','file']

class RateSubmissionForm(forms.ModelForm):
    """
        Formularz do oceniania zadania przez nauczyciela.

        Pola:
            grade (FloatField): Pole do wprowadzenia oceny.
            comment (CharField): Pole do wprowadzenia komentarza.

    """

    class Meta:
        model = RateSubmission
        fields = ['grade', 'comment']
        widgets = {
            'grade': forms.NumberInput(attrs={'class': 'custom_grade_input', 'placeholder': 'Wprowadź ocene'}),
            'comment': forms.Textarea(attrs={'class': 'custom_comment_textarea', 'placeholder': 'Wprowadź komentarz'}),
        }

class TopicForm(forms.ModelForm):
    """
        Formularz do tworzenia nowego tematu.

        Pola:
            title (CharField): Pole do wprowadzenia tytułu tematu.
            content (TextField): Pole do wprowadzenia treści tematu.

    """

    class Meta:
        model = Topic
        fields = ['title','content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'custom_title_class', 'placeholder': 'Wprowadź tytuł'}),
            'content': forms.Textarea(attrs={'class': 'custom_content_class', 'placeholder': 'Wprowadź opis'}),
        }