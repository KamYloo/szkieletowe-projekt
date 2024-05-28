from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import shutil
import os
from PIL import Image
from django.core.files.storage import default_storage as storage
from io import BytesIO

class Topic(models.Model):
    """
       Model reprezentujący temat kursu.

       Atrybuty:
           title (CharField): Tytuł tematu.
           content (CharField): Treść tematu.
           files (ManyToManyField): Pliki powiązane z tematem.
           assignments (ManyToManyField): Zadania powiązane z tematem.

       Metody:
           __str__(): Zwraca czytelną reprezentację tematu, czyli jego tytuł.

    """
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024, blank=True)
    files = models.ManyToManyField('CourseFile',blank=True)
    assignments = models.ManyToManyField('Assignment',blank=True)

    def __str__(self):
        return f"{self.title}"

class File(models.Model):
    """
       Model reprezentujący plik.

       Atrybuty:
           file (FileField): Pole pliku, przechowuje fizyczny plik.

       Metody:
           __str__(): Zwraca czytelną reprezentację pliku, czyli jego nazwę.

    """
    file = models.FileField(upload_to='pdf_files/')

    def __str__(self):
        return f"{self.file.name}"

class CourseFile(models.Model):
    """
        Model reprezentujący plik kursu.

        Atrybuty:
            name (CharField): Nazwa pliku.
            file (FileField): Pole pliku, przechowuje fizyczny plik.

        Metody:
            __str__(): Zwraca czytelną reprezentację pliku kursu, czyli jego nazwę.

    """
    name = models.CharField(max_length=64, blank=False)
    file = models.FileField(upload_to='pdf_files/')

    def __str__(self):
        return f"{self.name}"

class Assignment(models.Model):
    """
       Model reprezentujący zadanie.

       Atrybuty:
           title (CharField): Tytuł zadania.
           content (CharField): Treść zadania.
           due_date (DateTimeField): Termin wykonania zadania.
           topics (ManyToManyField): Tematy związane z zadaniem.

       Metody:
           __str__(): Zwraca czytelną reprezentację zadania, czyli jego tytuł.

    """
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    due_date = models.DateTimeField(default=datetime.now() + timedelta(weeks=1))
    topics = models.ManyToManyField('Topic', blank=True)

    def __str__(self):
        return f"{self.title}"

class Submission(models.Model):
    """
        Model reprezentujący zgłoszenie zadania.

        Atrybuty:
            assignment (ForeignKey): Powiązanie z modelem Assignment, określa zadanie, do którego odnosi się zgłoszenie.
            student (ForeignKey): Powiązanie z modelem User, określa użytkownika, który przesłał zgłoszenie.
            submission_date (DateTimeField): Data i czas przesłania zgłoszenia, ustawiana automatycznie.
            file (FileField): Pole pliku, przechowuje przesłany plik.

        Metody:
            __str__(): Zwraca czytelną reprezentację zgłoszenia, zawierającą nazwę użytkownika i tytuł zadania.

    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
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
    """
       Model reprezentujący ocenę zgłoszenia zadania przez nauczyciela.

       Atrybuty:
           assignment (ForeignKey): Powiązanie z modelem Assignment, określa zadanie, które zostało ocenione.
           teacher (ForeignKey): Powiązanie z modelem Profile, określa nauczyciela, który wystawił ocenę.
           student (ForeignKey): Powiązanie z modelem User, określa użytkownika, którego zgłoszenie zostało ocenione.
           grade (FloatField): Ocena wystawiona przez nauczyciela, domyślnie ustawiona na 0.
           comment (CharField): Komentarz do oceny, maksymalnie 1024 znaki.

    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.FloatField(default=0)
    comment = models.CharField(max_length=1024)


class Semester(models.Model):
    """
        Model reprezentujący semestr.

        Atrybuty:
            semester (CharField): Nazwa semestru.

        Metody:
            __str__(): Zwraca czytelną reprezentację semestru, czyli jego nazwę.

    """

    semester = models.CharField(max_length=50)
    def __str__(self):
        return self.semester

class Degree(models.Model):
    """
        Model reprezentujący stopień naukowy.

        Atrybuty:
            degree (CharField): Nazwa stopnia naukowego.

        Metody:
            __str__(): Zwraca czytelną reprezentację stopnia naukowego, czyli jego nazwę.

    """
    degree = models.CharField(max_length=50)
    def __str__(self):
        return self.degree

class Course(models.Model):
    """
       Model reprezentujący kurs.

       Atrybuty:
           teacher (ForeignKey): Powiązanie z modelem Profile, określa nauczyciela prowadzącego kurs.
           topics (ManyToManyField): Powiązanie z modelem Topic, określa tematy związane z kursem.
           title (CharField): Tytuł kursu.
           description (TextField): Opis kursu.
           semester (ForeignKey): Powiązanie z modelem Semester, określa semestr, do którego przypisany jest kurs.
           degree (ForeignKey): Powiązanie z modelem Degree, określa stopień naukowy, do którego przypisany jest kurs.
           image (ImageField): Obraz reprezentujący kurs.
           access_key (CharField): Klucz dostępu do kursu.

       Metody:
           __str__(): Zwraca czytelną reprezentację kursu, czyli jego tytuł.
           save(): Przeskalowuje obraz kursu do odpowiednich wymiarów przed zapisaniem.

    """
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True, default="course_images/default_course.jpg")
    access_key = models.CharField(max_length=50)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)

        image_read = storage.open(self.image.name, "r")
        img = Image.open(image_read)

        if img.height > 612 or img.width > 408:
            imageBuffer = BytesIO()
            output_size = (612, 408)
            img.thumbnail(output_size)
            img.save(imageBuffer, img.format)

        image_read.close()

class Enrollment(models.Model):
    """
        Model reprezentujący zapis użytkownika na kurs.

        Atrybuty:
            student (ForeignKey): Powiązanie z modelem User, określa użytkownika zapisanego na kurs.
            course (ForeignKey): Powiązanie z modelem Course, określa kurs, na który użytkownik jest zapisany.
            access_key (CharField): Klucz dostępu do kursu.
            joined_at (DateTimeField): Data i czas dołączenia użytkownika do kursu, ustawiana automatycznie.

    """
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    access_key = models.CharField(max_length=50)
    joined_at = models.DateTimeField(auto_now_add=True)




