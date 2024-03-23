from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Assignment, Submission
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import SubmissionForm
# Create your views here.

def index(request):
    return render(request, "cez/index.html")

# def assignment(request):
#     return render(request, "cez/assignment.html", {"assignments": Assignment.objects.all()})

class AssignmentListView(ListView):
    model = Assignment
    template_name = "cez/assignment.html"
    context_object_name = "assignments"


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



