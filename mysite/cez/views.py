import os
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Assignment, Submission, Topic, File
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import SubmissionForm,TopicUpdateForm, AssignmentForm, AssignmentUpdateForm, FileForm
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
# Create your views here.

def index(request):
    return render(request, "cez/index.html")

def course(request):
    return render(request, "cez/courses.html")

def create_course(request):
    return render(request, "cez/create_course_form.html")

# def assignment(request):
#     return render(request, "cez/assignment.html", {"assignments": Assignment.objects.all()})

class AssignmentListView(ListView):
    model = Assignment
    template_name = "cez/assignment.html"
    context_object_name = "assignments"

class TopicListView(ListView):
    model = Topic
    template_name = "cez/topic.html"
    context_object_name = "topics"

def view_topic(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        messages.error(request, 'Topic does not exist')
        return redirect('topic')
    return render(request, "cez/topic_detail.html", {"topic":topic, "files": topic.files.all(), "assignments": topic.assignments.all()})

def create_assignments(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save()
            assignment.topics.add(topic)
            topic.assignments.add(assignment)
            assignment.save()
            topic.save()
            return redirect('topic-detail', topic_id=topic_id)
    else:
        form = AssignmentForm()
    return render(request, 'cez/create_assignment.html', {'form': form, 'topic': topic})

def submit_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(pk=assignment_id)
    except Assignment.DoesNotExist:
        messages.error(request, 'Assignment does not exist')
        return redirect('assignment')
    submission_instance = Submission.objects.filter(assignment=assignment, student=request.user.profile).first()
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission_instance)
        if form.is_valid():
            form.instance.assignment = assignment
            form.instance.student = request.user.profile
            form.save()
            messages.success(request, 'Your answer has been submitted!')
            return redirect('assignment')
    else:
        form = SubmissionForm(instance=submission_instance)
    return render(request, 'cez/submit_assignment.html', {'form': form, 'assignment':assignment})

def update_assignment(request, assignment_id):
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
            return redirect('assignment')
    else:
        form = AssignmentUpdateForm(instance=assignment)
    return render(request, 'cez/update_assignment.html', {'form': form, 'assignment':assignment})


@user_passes_test(lambda u: u.groups.filter(name='Nauczyciel').exists())
def update_topic(request, topic_id):
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
            return redirect('topic-detail', topic_id)
    else:
        form = TopicUpdateForm(instance=topic)
    return render(request, 'cez/topic_update.html', {'form': form}) # , 'topic': topic

def add_file(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        messages.error(request, 'Topic does not exist')
        return redirect('topic')
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            topic.files.add(file)
            topic.save()
            messages.success(request, 'File added')
            return redirect('topic-detail', topic_id)
    else:
        form = FileForm()
    return render(request, 'cez/add_file.html', {'form': form})

def delete_file(request, topic_id, file_id):
    file = File.objects.get(pk=file_id)
    # os.remove(file.file.path)
    file.file.delete()
    file.delete()
    messages.success(request, "Deleted file")
    return redirect('topic-detail', topic_id)
