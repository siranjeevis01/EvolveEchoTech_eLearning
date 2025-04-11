from django.views.generic import ListView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.template import TemplateDoesNotExist
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.tokens import default_token_generator
import logging
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView
from django.utils.decorators import method_decorator
from django.template.loader import get_template

from .forms import (
    EnrollmentForm, ReviewForm, SignUpForm, SignInForm, ForgotPasswordForm, PasswordResetForm,
    ContactForm
)
from .models import CustomUser, Course, Enrollment, Review
from .utils import send_reset_password_email

User = get_user_model()
logger = logging.getLogger(__name__)

class SignupView(FormView):
    template_name = 'myapp/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('signin')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Sign Up successful. Please login.')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SigninView(FormView):
    template_name = 'myapp/signin.html'
    form_class = SignInForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        logger.debug(f"Form data: {form.cleaned_data}")
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        logger.debug(f"Authenticated user: {user}")

        if user is not None:
            login(self.request, user)
            logger.debug(f"User logged in: {self.request.user}")
            messages.success(self.request, 'Signin successful.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Sign in failed. Please correct the errors below.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.debug(f"Form invalid: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))


class SignoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request) 
        messages.success(request, 'You have been signed out.')  
        return redirect('index')  

class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'myapp/forgot_password.html', {'form': form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                send_reset_password_email(user)
                return redirect('forgot_password_done')
            return render(request, 'myapp/forgot_password.html', {'form': form, 'error': 'Email address not found.'})
        return render(request, 'myapp/forgot_password.html', {'form': form, 'error': 'Invalid email address.'})

class ForgotPasswordDoneView(View):
    def get(self, request):
        return render(request, 'myapp/forgot_password_done.html')

class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = PasswordResetForm()
            return render(request, 'myapp/reset_password.html', {'form': form, 'user': user})
        else:
            return redirect('myapp/reset_password_invalid')

    def post(self, request, uidb64, token):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password']
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                return redirect('reset_password_done')
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return redirect('reset_password_invalid')
        return render(request, 'myapp/reset_password.html', {'form': form})

class PasswordResetCompleteView(View):
    def get(self, request):
        return render(request, 'myapp/reset_password_done.html')

class PasswordResetInvalidView(View):
    def get(self, request):
        return render(request, 'myapp/reset_password_invalid.html')

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'myapp/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['recipient@example.com'],
                fail_silently=False,
            )
            return redirect('contact_success')
        return render(request, 'myapp/contact.html', {'form': form})

class ContactSuccessView(View):
    def get(self, request):
        return render(request, 'myapp/contact_success.html')

class IndexView(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.all()
        print(f"Courses: {courses}") 
        context['courses'] = courses
        return context

class AboutView(TemplateView):
    template_name = 'myapp/about.html'

class TestimonialView(View):
    def get(self, request):
        return render(request, 'myapp/testimonial.html')

class PageNotFoundView(TemplateView):
    template_name = 'myapp/page_not_found.html'

class GenericCourseView(TemplateView):
    def get_template_names(self):
        slug = self.kwargs.get('read_more_slug')
        template_name = f"myapp/{slug}.html"
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            raise Http404(f"Template {template_name} does not exist.")
        return [template_name]

class SlugPageView(TemplateView):
    template_name = ''

    def get_template_names(self):
        slug = self.kwargs.get('slug')
        template_name = f"myapp/{slug}.html"
        try:
            self.template_name = template_name
            return [self.template_name]
        except:
            raise Http404(f"Template {template_name} does not exist.")
        
class EnrollmentView(LoginRequiredMixin, View):
    template_name = 'myapp/enroll.html'

    def get(self, request, *args, **kwargs):
        join_now_slug = self.kwargs.get('join_now_slug') 
        return render(request, f"myapp/{join_now_slug}.html")  

    def post(self, request, *args, **kwargs):
        join_now_slug = self.kwargs.get('join_now_slug')
        course = get_object_or_404(Course, join_now_slug=join_now_slug)

        enrollment = Enrollment(
            user=request.user, 
            course=course,
            course_title=course,
            full_name=request.POST.get('full_name'),
            dob=request.POST.get('dob'),
            gender=request.POST.get('gender'),
            area=request.POST.get('area'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            phone_number=request.POST.get('phone_number'),
            email=request.POST.get('email'),
            emergency_contact_name=request.POST.get('emergency_contact_name'),
            relationship=request.POST.get('relationship'),
            emergency_phone_number=request.POST.get('emergency_phone_number'),
            course_framework=request.POST.get('course_framework'),
            start_date=request.POST.get('start_date'),
            highest_education=request.POST.get('highest_education'),
            institution_name=request.POST.get('institution_name'),
            graduation_year=request.POST.get('graduation_year'),
            employment_status=request.POST.get('employment_status'),
            employer_details=request.POST.get('employer_details'),
            hear_about_course=request.POST.get('hear_about_course'),
        )

        if enrollment.full_name and enrollment.email: 
            enrollment.save()
            messages.success(request, 'Enrollment successful!')
            return redirect('course_confirmation', enrollment_id=enrollment.id)
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, f"myapp/{join_now_slug}.html", {'enrollment': enrollment}) 

class CourseConfirmationView(TemplateView):
    template_name = 'myapp/course_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrollment_id = self.kwargs.get('enrollment_id')
        registration = get_object_or_404(Enrollment, id=enrollment_id)
        course = get_object_or_404(Course, id=registration.course.id)

        context['registration'] = registration
        context['course'] = course
        return context

class CoursesView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'myapp/courses.html'
    context_object_name = 'enrolled_courses'

    def get_queryset(self):
        # Get all the enrollments for the logged-in user
        return Enrollment.objects.filter(user=self.request.user).select_related('course')


def csrf_failure(request, reason=""):
    return render(request, 'myapp/csrf_failure.html', status=403)


class SubmitReviewView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        course_id = request.GET.get('course_id')
        if not course_id or not course_id.isdigit():
            return render(request, 'page_not_found.html', {'error': 'Invalid Course ID'})

        course = get_object_or_404(Course, id=course_id)
        return render(request, 'review_form.html', {'course': course})

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        review = Review(course=course, user=request.user, rating=rating, comment=comment)
        review.save()

        messages.success(request, 'Review submitted successfully!')
        return redirect('course_detail', slug=course.join_now_slug)
