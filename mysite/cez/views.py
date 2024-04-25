import logging
from datetime import datetime

from django.shortcuts import render,redirect,get_object_or_404
from .models import Course, Enrollment, CourseFile
from .models import Assignment, Submission, Topic, File, RateSubmission
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import SubmissionForm,TopicUpdateForm, AssignmentForm, AssignmentUpdateForm, FileForm, RateSubmissionForm, TopicForm, CourseForm, AccessKeyForm, CourseFileForm
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.db.models import Q
# Create your views here.

logger = logging.getLogger(__name__)

def index(request):
    """
        Widok strony głównej.

        Pobiera liczbę kursów, użytkowników i tematów z bazy danych
        i renderuje szablon HTML dla strony głównej.

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.

        Zwraca:
            HttpResponse: Odpowiedź HTTP zawierająca zawartość strony głównej.
    """
    num_courses = Course.objects.count()
    num_users = User.objects.count()
    num_topics = Topic.objects.count()
    context = {
        'is_homepage': True,
        'num_courses': num_courses,
        'num_users': num_users,
        'num_topics': num_topics
    }

    return render(request, 'cez/index.html', context)


def courses(request):
    """
       Widok strony kursów.

       Pobiera parametry zapytania GET (tytuł, identyfikator stopnia, identyfikator semestru)
       i zwraca odpowiednie kursy zgodnie z filtrami.

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.

       Zwraca:
           HttpResponse: Odpowiedź HTTP zawierająca zawartość strony kursów.
    """
    title = request.GET.get("title")
    degree_id = request.GET.get("degree_id")
    semester_id = request.GET.get("semester_id")
    if (title == '' or title == None) and degree_id == None and semester_id == None :
        courses = Course.objects.all()
    else:
        query = Q()
        if title != '' and title != None:
            query &= Q(title__icontains=title)
        if degree_id != None:
            query &= Q(degree_id=degree_id)
        if semester_id != None:
            query &= Q(semester_id=semester_id)
        courses = Course.objects.filter(query)
    return render(request, 'cez/courses.html', {'courses': courses, 'title': title})


@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def create_assignments(request, course_id, topic_id):
    """
    Widok tworzenia zadań.

    Wymagane uprawnienia:
        - Użytkownik musi być przypisany do grupy "Nauczyciel".

    Argumenty:
        request (HttpRequest): Obiekt żądania HTTP.
        course_id (int): Identyfikator kursu, do którego przypisane jest nowe zadanie.
        topic_id (int): Identyfikator tematu, do którego przypisane jest nowe zadanie.

    Zwraca:
        render: Renderowany szablon zawierający formularz tworzenia zadania.

    Opis działania:
        Ten widok obsługuje tworzenie nowych zadań. Najpierw pobiera temat o podanym identyfikatorze.
        Następnie sprawdza, czy żądanie jest typu POST. Jeśli tak, przetwarza formularz tworzenia zadania.
        Po walidacji formularza, zapisuje nowe zadanie oraz aktualizuje listę zadań przypisanych do tematu.
        Na koniec wyświetla komunikat o sukcesie i przekierowuje użytkownika na stronę szczegółów kursu.

    """
    topic = Topic.objects.get(pk=topic_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.save()
            assignment.topics.add(topic)
            topic.assignments.add(assignment)
            topic.save()
            messages.success(request, 'Assignment has been created successfully!')
            logger.info(f'Assignment has been created successfully by {request.user}.')
            return redirect('course_detail', course_id=course_id)
    else:
        form = AssignmentForm()
    return render(request, 'cez/create_assignment.html', {'form': form, 'topic': topic})


@login_required
def submit_assignment(request, assignment_id):
    """
       Widok odpowiedzialny za przesyłanie odpowiedzi na zadanie.

       Wymagane uprawnienia:
           - Użytkownik musi być zalogowany.

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.
           assignment_id (int): Identyfikator zadania.

       Zwraca:
           HttpResponse: Renderowany szablon strony przesyłania odpowiedzi na zadanie.

       Opis działania:
           Ten widok obsługuje przesyłanie odpowiedzi na zadanie. Sprawdza, czy zadanie
           o podanym identyfikatorze istnieje. Następnie sprawdza, czy użytkownik
           już przesłał odpowiedź na to zadanie. Jeśli tak, pobiera ocenę przypisaną do
           odpowiedzi. Gdy żądanie jest typu POST, przetwarza formularz przesłanej
           odpowiedzi. Po walidacji formularza, przypisuje odpowiednie wartości i zapisuje
           odpowiedź. Po zapisaniu, wyświetla komunikat potwierdzający przesłanie odpowiedzi
           i rejestruje to zdarzenie w logach. W przeciwnym razie, generuje formularz
           dla przesłanej odpowiedzi.

       Wyjątki:
           Assignment.DoesNotExist: W przypadku braku istnienia zadania, wyświetlany jest
               komunikat o błędzie, a użytkownik jest przekierowywany na stronę główną.

    """

    try:
        assignment = Assignment.objects.get(pk=assignment_id)
        submission_instance = Submission.objects.filter(assignment_id=assignment.id, student=request.user).first()
    except Assignment.DoesNotExist:
        messages.error(request, 'Assignment does not exist')
        return redirect('index')

    grade = 0
    if submission_instance:
        grade = RateSubmission.objects.filter(assignment_id=assignment_id, student_id=request.user.id).first()

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission_instance)
        if form.is_valid():
            form.instance.assignment = assignment
            form.instance.student = request.user
            form.save()
            messages.success(request, 'Your answer has been submitted!')
            logger.info(f'User {request.user} submitted assignment {assignment}.')
            return redirect('assignment-submit', assignment_id)
    else:
        form = SubmissionForm(instance=submission_instance)

    return render(request, 'cez/submit_assignment.html', {'form': form, 'assignment': assignment, 'grade': grade})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def create_course(request):
    """
       Widok odpowiedzialny za tworzenie nowego kursu.

       Wymagane uprawnienia:
           - Użytkownik musi być zalogowany.
           - Użytkownik musi być przypisany do grupy "Nauczyciel".

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.

       Zwraca:
           HttpResponse: Renderowany szablon formularza tworzenia kursu.

       Opis działania:
           Ten widok obsługuje tworzenie nowego kursu. Sprawdza, czy żądanie jest typu POST.
           Jeśli tak, przetwarza formularz danych kursu. Po walidacji formularza, zapisuje
           nowy kurs oraz przypisuje użytkownika jako nauczyciela tego kursu. Tworzy również
           wpis o zapisie użytkownika na kurs. Po zapisaniu, rejestruje to zdarzenie w logach
           i przekierowuje użytkownika na stronę z listą kursów. W przeciwnym razie, generuje
           pusty formularz dla tworzenia kursu.

    """

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user.profile
            course.save()
            enrollment = Enrollment.objects.create(student=request.user, course=course)
            enrollment.save()
            logger.info(f'User {request.user} created course {course}.')
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'cez/create_course_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def delete_course(request, course_id):
    """
       Widok odpowiedzialny za usuwanie kursu.

       Wymagane uprawnienia:
           - Użytkownik musi być zalogowany.
           - Użytkownik musi być przypisany do grupy "Nauczyciel".

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.
           course_id (int): Identyfikator kursu do usunięcia.

       Zwraca:
           HttpResponseRedirect: Przekierowanie na stronę z listą kursów.

       Opis działania:
           Ten widok obsługuje usuwanie kursu. Najpierw pobiera kurs o podanym identyfikatorze.
           Następnie usuwa ten kurs z bazy danych. Po usunięciu, wyświetla komunikat o sukcesie
           oraz rejestruje to zdarzenie w logach. Na koniec przekierowuje użytkownika na stronę
           z listą kursów.

    """

    course = Course.objects.get(pk=course_id)
    course.delete()
    messages.success(request, "Deleted course")
    logger.info(f'User {request.user} deleted course {course}.')
    return redirect('courses')


@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def update_assignment(request, course_id, assignment_id):
    """
       Widok odpowiedzialny za aktualizację zadania.

       Wymagane uprawnienia:
           - Użytkownik musi być przypisany do grupy "Nauczyciel".

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.
           course_id (int): Identyfikator kursu, do którego należy zadanie.
           assignment_id (int): Identyfikator zadania do aktualizacji.

       Zwraca:
           HttpResponse: Renderowany szablon formularza aktualizacji zadania.

       Opis działania:
           Ten widok obsługuje aktualizację istniejącego zadania. Sprawdza, czy zadanie
           o podanym identyfikatorze istnieje. Jeśli nie, wyświetla komunikat o błędzie
           i rejestruje to zdarzenie w logach. Gdy żądanie jest typu POST, przetwarza
           formularz aktualizacji zadania. Po walidacji formularza, zapisuje zmiany
           w zadaniu. Po zapisaniu, wyświetla komunikat o sukcesie i rejestruje to
           zdarzenie w logach. W przeciwnym razie, generuje formularz aktualizacji
           zadania.

       Wyjatki:
       Assignment.DoesNotExist: W przypadku braku istnienia zadania, wyświetlany jest
            komunikat o błędzie, a użytkownik jest przekierowywany na stronę główną.


    """

    try:
        assignment = Assignment.objects.get(pk=assignment_id)
    except Assignment.DoesNotExist:
        messages.error(request, 'Assignment does not exist')
        logger.info(f'User {request.user} tried to update assignment which does not exist.')
        return redirect('assignment')
    if request.method == 'POST':
        form = AssignmentUpdateForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your have updated the assignment')
            logger.info(f'User {request.user} updated assignment {assignment}.')
            return redirect('course_detail', course_id)
    else:
        form = AssignmentUpdateForm(instance=assignment)
    return render(request, 'cez/update_assignment.html', {'form': form, 'assignment':assignment})


@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def remove_assignment(request, course_id, assignment_id):
    """
       Widok odpowiedzialny za usuwanie zadania.

       Wymagane uprawnienia:
           - Użytkownik musi być przypisany do grupy "Nauczyciel".

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.
           course_id (int): Identyfikator kursu, do którego należy zadanie.
           assignment_id (int): Identyfikator zadania do usunięcia.

       Zwraca:
           HttpResponseRedirect: Przekierowanie na stronę szczegółów kursu.

       Opis działania:
           Ten widok obsługuje usuwanie istniejącego zadania. Najpierw pobiera zadanie
           o podanym identyfikatorze. Następnie usuwa to zadanie z bazy danych. Po usunięciu,
           wyświetla komunikat o sukcesie oraz rejestruje to zdarzenie w logach. Na koniec
           przekierowuje użytkownika na stronę szczegółów kursu.

    """

    assignment = Assignment.objects.get(pk=assignment_id)
    logger.info(f'User {request.user} deleted assignment {assignment}.')
    assignment.delete()
    messages.success(request, "Deleted assignment")
    return redirect('course_detail', course_id)

@login_required
def enroll_to_course(request, course_id):
    """
        Widok odpowiedzialny za zapisanie się na kurs.

        Wymagane uprawnienia:
            - Użytkownik musi być zalogowany.

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.
            course_id (int): Identyfikator kursu, na który użytkownik chce się zapisać.

        Zwraca:
            HttpResponseRedirect: Przekierowanie na stronę szczegółów kursu lub renderowany szablon
                formularza dostępu do kursu w przypadku konieczności podania klucza dostępu.

        Opis działania:
            Ten widok obsługuje zapisanie użytkownika na kurs. Sprawdza, czy użytkownik już jest
            zapisany na ten kurs. Jeśli nie, sprawdza, czy żądanie jest typu POST. Jeśli tak,
            przetwarza formularz dostępu do kursu. Jeśli klucz dostępu jest poprawny, tworzy wpis
            o zapisie użytkownika na kurs. Po zapisaniu, rejestruje to zdarzenie w logach i przekierowuje
            użytkownika na stronę szczegółów kursu. W przeciwnym razie, wyświetla formularz dostępu do kursu.

        Wyjątki:
        Enrollment.DoesNotExist: W przypadku braku istnienia wpisu o zapisie użytkownika na kurs,
            użytkownik jest proszony o podanie klucza dostępu lub przekierowywany na stronę
            szczegółów kursu.
    """
    course = Course.objects.get(pk=course_id)
    participants = Enrollment.objects.filter(course_id=course_id)
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        if request.method == 'POST':
            form = AccessKeyForm(request.POST)
            if form.is_valid():
                access_key = form.cleaned_data['access_key']
                if access_key == course.access_key:
                    enrollment = Enrollment.objects.create(student=request.user, course=course)
                    enrollment.save()
                    logger.info(f'User {request.user} enrolled in course {course} at {datetime.now()}')
                    return redirect('course_detail', course_id=course.id)
                else:
                    logger.info(
                        f'User {request.user} tried to enrolled in course {course} but the password was invalid.'
                    )
                    form.add_error(None, 'Invalid access key')
        else:
            form = AccessKeyForm()
        return render(request, 'cez/enroll_to_course.html', {'form': form, 'participants': participants})
    return redirect('course_detail', course_id=course_id)

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def update_topic(request, course_id, topic_id):
    """
       Widok odpowiedzialny za aktualizację tematu kursu.

       Wymagane uprawnienia:
           - Użytkownik musi być przypisany do grupy "Nauczyciel".

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.
           course_id (int): Identyfikator kursu, do którego należy temat.
           topic_id (int): Identyfikator tematu do aktualizacji.

       Zwraca:
           HttpResponseRedirect: Przekierowanie na stronę szczegółów kursu po zaktualizowaniu tematu.

       Opis działania:
           Ten widok obsługuje aktualizację istniejącego tematu kursu. Najpierw pobiera temat
           o podanym identyfikatorze. Następnie sprawdza, czy żądanie jest typu POST. Jeśli tak,
           przetwarza formularz aktualizacji tematu. Po walidacji formularza, zapisuje zmiany w temacie.
           Po zapisaniu, wyświetla komunikat o sukcesie i rejestruje to zdarzenie w logach. W przeciwnym
           razie, generuje formularz aktualizacji tematu.

       Wyjątki:
           Topic.DoesNotExist: W przypadku braku istnienia tematu, wyświetlany jest komunikat o błędzie,
               a użytkownik jest przekierowywany na stronę szczegółów kursu.

    """

    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        logger.info(
            f'User {request.user} tried to update topic of id {topic_id} but it does not exist.'
        )
        messages.error(request, 'Topic does not exist')
        return redirect('course_detail', course_id)
    if request.method == 'POST':
        form = TopicUpdateForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            logger.info(f'User {request.user} update topic {topic}.')
            messages.success(request, 'Topic updated')
            return redirect('course_detail', course_id)
    else:
        form = TopicUpdateForm(instance=topic)
    return render(request, 'cez/topic_update.html', {'form': form}) # , 'topic': topic

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def add_file(request, course_id, topic_id):
    """
        Widok odpowiedzialny za dodanie pliku do tematu kursu.

        Wymagane uprawnienia:
            - Użytkownik musi być przypisany do grupy "Nauczyciel".

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.
            course_id (int): Identyfikator kursu, do którego należy temat.
            topic_id (int): Identyfikator tematu, do którego dodawany jest plik.

        Zwraca:
            HttpResponseRedirect: Przekierowanie na stronę szczegółów kursu po dodaniu pliku.

        Opis działania:
            Ten widok obsługuje dodawanie pliku do istniejącego tematu kursu. Najpierw pobiera temat
            o podanym identyfikatorze. Następnie sprawdza, czy żądanie jest typu POST. Jeśli tak,
            przetwarza formularz dodawania pliku. Po walidacji formularza, zapisuje plik oraz dodaje go
            do listy plików tematu. Po zapisaniu, wyświetla komunikat o sukcesie i przekierowuje
            użytkownika na stronę szczegółów kursu.

        Wyjątki:
            Topic.DoesNotExist: W przypadku braku istnienia tematu, wyświetlany jest komunikat o błędzie,
                a użytkownik jest przekierowywany na stronę szczegółów kursu.

    """

    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        messages.error(request, 'Topic does not exist')
        return redirect('course_detail', course_id)
    if request.method == 'POST':
        form = CourseFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            topic.files.add(file)
            topic.save()
            messages.success(request, 'File added')
            return redirect('course_detail', course_id)
    else:
        form = CourseFileForm()
    return render(request, 'cez/add_file.html', {'form': form})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def delete_file(request, course_id, file_id):
    """
        Widok odpowiedzialny za usuwanie pliku z kursu.

        Wymagane uprawnienia:
            - Użytkownik musi być przypisany do grupy "Nauczyciel".

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.
            course_id (int): Identyfikator kursu, z którego usuwany jest plik.
            file_id (int): Identyfikator pliku do usunięcia.

        Zwraca:
            HttpResponseRedirect: Przekierowanie na stronę szczegółów kursu po usunięciu pliku.

        Opis działania:
            Ten widok obsługuje usuwanie pliku z kursu. Najpierw pobiera plik o podanym identyfikatorze.
            Następnie usuwa fizyczny plik z systemu plików oraz wpis o pliku z bazy danych. Po usunięciu,
            wyświetla komunikat o sukcesie i przekierowuje użytkownika na stronę szczegółów kursu.

    """

    file = CourseFile.objects.get(pk=file_id)
    file.file.delete()
    file.delete()
    messages.success(request, "Deleted file")
    return redirect('course_detail', course_id)

@login_required
def course_detail(request, course_id):
    """
        Widok szczegółów kursu.

        Wymagane uprawnienia:
            - Użytkownik musi być zalogowany.

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.
            course_id (int): Identyfikator kursu, którego szczegóły są wyświetlane.

        Zwraca:
            render: Renderowany szablon zawierający szczegóły kursu.

        Opis działania:
            Ten widok obsługuje wyświetlanie szczegółów kursu. Najpierw pobiera kurs o podanym identyfikatorze.
            Następnie pobiera tematy oraz uczestników kursu. Na koniec renderuje szablon zawierający szczegóły kursu
            wraz z listą tematów i uczestników.

    """

    course = Course.objects.get(pk=course_id)
    topics = Course.objects.get(pk=course_id).topics.all()
    participants = Enrollment.objects.filter(course_id=course_id)
    return render(request, 'cez/course_detail.html', {'course': course, 'topics': topics, 'user': request.user, 'participants': participants})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def rate_assignment(request, course_id, assignment_id):
    """
        Widok oceniania zadania.

        Wymagane uprawnienia:
            - Użytkownik musi być przypisany do grupy "Nauczyciel".

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.
            course_id (int): Identyfikator kursu, do którego należy zadanie.
            assignment_id (int): Identyfikator zadania do ocenienia.

        Zwraca:
            render: Renderowany szablon zawierający formularz oceny zadania.

        Opis działania:
            Ten widok obsługuje ocenianie zadania. Najpierw pobiera zadanie o podanym identyfikatorze.
            Następnie pobiera wszystkie zgłoszenia związane z tym zadaniem. Na koniec renderuje szablon
            zawierający formularz oceniania zadania oraz listę zgłoszeń.

    """

    assignment = Assignment.objects.get(pk=assignment_id)
    submissions = Submission.objects.filter(assignment__id=assignment.id)
    return render(request, 'cez/rate_assignment.html', {'assignment': assignment,'submissions': submissions, 'course_id': course_id})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def rate_users_assignment(request, course_id, assignment_id, submission_id):
    """
       Widok odpowiedzialny za ocenianie zadań użytkowników.

       Wymagane uprawnienia:
           - Użytkownik musi być przypisany do grupy "Nauczyciel".

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.
           course_id (int): Identyfikator kursu, do którego należy zadanie.
           assignment_id (int): Identyfikator zadania, które jest oceniane.
           submission_id (int): Identyfikator zgłoszenia, które jest oceniane.

       Zwraca:
           HttpResponseRedirect: Przekierowanie na stronę oceniania zadań.

       Opis działania:
           Ten widok obsługuje ocenianie zadań użytkowników. Najpierw pobiera zgłoszenie o podanym
           identyfikatorze. Następnie sprawdza, czy istnieje już ocena dla tego zgłoszenia od danego
           nauczyciela. Jeśli tak, używa istniejącego formularza oceny. W przeciwnym razie, generuje
           nowy formularz oceny. Gdy żądanie jest typu POST i formularz jest poprawny, zapisuje ocenę
           i przekierowuje użytkownika na stronę oceniania zadań.

       Wyjątki:
       RateSubmission.DoesNotExist: W przypadku braku istnienia oceny dla danego zgłoszenia od danego nauczyciela,
            generowany jest nowy formularz oceny.
    """

    submission = get_object_or_404(Submission, pk=submission_id)

    try:
        existing_rating = RateSubmission.objects.get(assignment_id=assignment_id,
                                                     teacher=request.user.profile,
                                                     student_id=submission.student.pk)
    except RateSubmission.DoesNotExist:
        existing_rating = None

    if request.method == 'POST':
        if existing_rating:
            form = RateSubmissionForm(request.POST, instance=existing_rating)
        else:
            form = RateSubmissionForm(request.POST)

        if form.is_valid():
            form.instance.teacher = request.user.profile
            form.instance.student = submission.student
            form.instance.assignment = Assignment.objects.get(pk=assignment_id)
            form.save()
            logger.info(f'User {request.user} has rated assignment of id {assignment_id} and submission id {submission_id}.')
            return redirect('assignment-rate', course_id=course_id, assignment_id=assignment_id)
    else:
        form = RateSubmissionForm(instance=existing_rating)

    return render(request, 'cez/rate_students_assignment.html', {'form': form, 'submission': submission})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def add_topic(request, course_id):
    """
       Widok odpowiedzialny za dodanie nowego tematu do kursu.

       Wymagane uprawnienia:
           - Użytkownik musi być przypisany do grupy "Nauczyciel".

       Argumenty:
           request (HttpRequest): Obiekt żądania HTTP.
           course_id (int): Identyfikator kursu, do którego dodawany jest temat.

       Zwraca:
           HttpResponseRedirect: Przekierowanie na stronę szczegółów kursu po dodaniu tematu.

       Opis działania:
           Ten widok obsługuje dodawanie nowego tematu do istniejącego kursu. Najpierw pobiera kurs
           o podanym identyfikatorze. Następnie sprawdza, czy żądanie jest typu POST. Jeśli tak,
           przetwarza formularz dodawania tematu. Po walidacji formularza, zapisuje nowy temat,
           dodaje go do listy tematów kursu oraz wyświetla komunikat o sukcesie. W przypadku żądania
           typu GET, generuje formularz dodawania tematu.

    """

    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save()
            topic.save()
            course.topics.add(topic)
            messages.success(request, 'Topic added')
            logger.info(f'User {request.user} added topic {topic}.')
            return redirect('course_detail', course_id)
    else:
        form = TopicForm()
    return render(request, 'cez/add_topic.html', {'form': form})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def delete_topic(request, course_id, topic_id):
    """
        Widok odpowiedzialny za usuwanie tematu z kursu.

        Wymagane uprawnienia:
            - Użytkownik musi być przypisany do grupy "Nauczyciel".

        Argumenty:
            request (HttpRequest): Obiekt żądania HTTP.
            course_id (int): Identyfikator kursu, z którego usuwany jest temat.
            topic_id (int): Identyfikator tematu do usunięcia.

        Zwraca:
            HttpResponseRedirect: Przekierowanie na stronę szczegółów kursu po usunięciu tematu.

        Opis działania:
            Ten widok obsługuje usuwanie tematu z kursu. Najpierw próbuje pobrać temat o podanym identyfikatorze.
            Następnie usuwa ten temat z bazy danych. Po usunięciu, wyświetla komunikat o sukcesie oraz rejestruje to
            zdarzenie w logach. Jeśli temat o podanym identyfikatorze nie istnieje, wyświetla komunikat o błędzie
            i rejestruje to zdarzenie w logach.

    """

    try:
        topic = Topic.objects.get(id=topic_id)
        topic.delete()
        messages.success(request, "Deleted topic")
        logger.info(f'User {request.user} has deleted topic {topic}.')
        return redirect('course_detail', course_id=course_id)
    except Topic.DoesNotExist:
        messages.error(request,"Topic does not exist.")
        logger.info(f'User {request.user} tried to delete topic of id {topic_id} but it does not exist.')
        return redirect('course_detail', course_id=course_id)