from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Course ,Enrollment
from .models import Assignment, Submission, Topic, File, RateSubmission
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import SubmissionForm,TopicUpdateForm, AssignmentForm, AssignmentUpdateForm, FileForm, RateSubmissionForm, TopicForm, CourseForm, AccessKeyForm, CourseFileForm
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.db.models import Q
# Create your views here.

def index(request):
    context = {
        'is_homepage': True
    }
    return render(request, 'cez/index.html', context)

def courses(request):
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
    topic = Topic.objects.get(pk=topic_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save()
            assignment.topics.add(topic)
            topic.assignments.add(assignment)
            assignment.save()
            topic.save()
            return redirect('course_detail', course_id)
    else:
        form = AssignmentForm()
    return render(request, 'cez/create_assignment.html', {'form': form, 'topic': topic})

@login_required
def submit_assignment(request, assignment_id):
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
            return redirect('assignment-submit', assignment_id)
    else:
        form = SubmissionForm(instance=submission_instance)

    return render(request, 'cez/submit_assignment.html', {'form': form, 'assignment': assignment, 'grade': grade})


@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user.profile
            course.save()
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'cez/create_course_form.html', {'form': form})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def update_assignment(request, course_id, assignment_id):
    try:
        assignment = Assignment.objects.get(pk=assignment_id)
    except Assignment.DoesNotExist:
        messages.error(request, 'Assignment does not exist')
        return redirect('assignment')
    if request.method == 'POST':
        form = AssignmentUpdateForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your have updated the assignment')
            return redirect('course_detail', course_id)
    else:
        form = AssignmentUpdateForm(instance=assignment)
    return render(request, 'cez/update_assignment.html', {'form': form, 'assignment':assignment})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def remove_assignment(request, course_id, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    assignment.delete()
    messages.success(request, "Deleted assignment")
    return redirect('course_detail', course_id)

@login_required
def enroll_to_course(request, course_id):
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
                    return redirect('course_detail', course_id=course.id)
                else:
                    form.add_error(None, 'Invalid access key')
        else:
            form = AccessKeyForm()
        return render(request, 'cez/enroll_to_course.html', {'form': form, 'participants': participants})
    return redirect('course_detail', course_id=course_id)

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def update_topic(request, course_id, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        messages.error(request, 'Topic does not exist')
        return redirect('topic')
    if request.method == 'POST':
        form = TopicUpdateForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated')
            return redirect('course_detail', course_id)
    else:
        form = TopicUpdateForm(instance=topic)
    return render(request, 'cez/topic_update.html', {'form': form}) # , 'topic': topic

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def add_file(request, course_id, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        messages.error(request, 'Topic does not exist')
        return redirect('topic')
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
    file = File.objects.get(pk=file_id)
    file.file.delete()
    file.delete()
    messages.success(request, "Deleted file")
    return redirect('course_detail', course_id)

@login_required
def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    topics = Course.objects.get(pk=course_id).topics.all()
    participants = Enrollment.objects.filter(course_id=course_id)
    return render(request, 'cez/course_detail.html', {'course': course, 'topics': topics, 'user': request.user, 'participants': participants})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def rate_assignment(request, course_id, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    submissions = Submission.objects.filter(assignment__id=assignment.id)
    return render(request, 'cez/rate_assignment.html', {'assignment': assignment,'submissions': submissions, 'course_id': course_id})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def rate_users_assignment(request, course_id, assignment_id, submission_id):
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
            return redirect('assignment-rate', course_id=course_id, assignment_id=assignment_id)
    else:
        form = RateSubmissionForm(instance=existing_rating)

    return render(request, 'cez/rate_students_assignment.html', {'form': form, 'submission': submission})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def add_topic(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save()
            topic.save()
            course.topics.add(topic)
            messages.success(request, 'Topic added')
            return redirect('course_detail', course_id)
    else:
        form = TopicForm()
    return render(request, 'cez/add_topic.html', {'form': form})

@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def delete_topic(request, course_id, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
        topic.delete()
        messages.success(request, "Deleted topic")
        return redirect('course_detail', course_id=course_id)
    except Topic.DoesNotExist:
        messages.error(request,"Topic does not exist.")
        return redirect('course_detail', course_id=course_id)