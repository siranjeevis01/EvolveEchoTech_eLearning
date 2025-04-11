from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('testimonial/', views.TestimonialView.as_view(), name='testimonial'),
    path('my_courses/', views.CoursesView.as_view(), name='enrolled_courses'), 
    path('read-more/<slug:read_more_slug>/', views.GenericCourseView.as_view(), name='read_more'),
    path('enroll/<slug:join_now_slug>/', views.EnrollmentView.as_view(), name='enroll_course'),
    path('courses/join/<slug:join_now_slug>/', views.EnrollmentView.as_view(), name='join_now_page'),
    path('enrollment/confirmation/<int:enrollment_id>/', views.CourseConfirmationView.as_view(), name='course_confirmation'),
    path('join-now/<slug:slug>/', views.SlugPageView.as_view(), name='slug_page'),
    

    path('submit_review/', views.SubmitReviewView.as_view(), name='submit_review'),



    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('forgot-password/done/', views.ForgotPasswordDoneView.as_view(), name='forgot_password_done'),
    
    path('reset-password/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='reset_password'),
    path('reset-password/done/', views.PasswordResetCompleteView.as_view(), name='reset_password_done'),
    path('reset-password-invalid/', views.PasswordResetInvalidView.as_view(), name='reset_password_invalid'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='myapp/forgot_password.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/forgot_password_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='myapp/reset_password.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='myapp/reset_password_done.html'), name='password_reset_complete'),

    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),

    path('404/', views.PageNotFoundView.as_view(), name='page_not_found'),
]
