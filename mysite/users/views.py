from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile
from django.db.models import Q
from cez.models import Course, Enrollment, Topic, Assignment, RateSubmission, Submission

from django.http import HttpResponse

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Please confirm your email address to complete the registration')
            return redirect('login')
    else:
        form = UserRegisterForm(request.POST)
        form.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
        form.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })
    return render(request, "users/register.html", {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Udało ci się aktywować konto!')
        return redirect('login')
    else:
        messages.error(request, 'Please confirm your email address to complete the registration')
        return redirect('register')

@login_required
def profile(request):
    enrollments = Enrollment.objects.filter(student_id=request.user).values_list('course_id', flat=True)
    course = Course.objects.filter(pk__in=enrollments)
    return render(request, 'users/profile.html', {'courses': course})

@login_required
def degrees(request):
    enrollments = Enrollment.objects.filter(student_id=request.user).values_list('course_id', flat=True)
    course = Course.objects.filter(pk__in=enrollments)
    return render(request, 'users/degrees.html', {'courses': course})

@login_required
def degrees_course(request, course_id):
    topics = Topic.objects.filter(course=course_id)
    assignments = Assignment.objects.filter(topic__in=topics)
    prof = Profile.objects.get(user_id=request.user.id)
    submission = Submission.objects.filter(Q(student_id=prof.id) & Q(assignment__in=assignments))

    # gradees = []
    # for assignment in assignments:
    #     gradees.append(RateSubmission.objects.filter(submission_id))

    gradees = RateSubmission.objects.filter(submission_id__in=submission).values_list('grade', flat=True)
    print(gradees)
    return render(request, 'users/degrees_course.html', {'assignments': assignments, 'gradees': gradees})

@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/updateprofile.html', {'u_form': u_form, 'p_form': p_form})