from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from datetime import date, timedelta
from django.utils.text import slugify

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_user_permissions'
AbstractUser._meta.get_field('groups').remote_field.related_name = 'auth_user_groups'
AbstractUser._meta.get_field('user_permissions').remote_field.related_name = 'auth_user_user_permissions'


class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at >= timezone.now() - timezone.timedelta(hours=1)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    image = models.ImageField(upload_to='instructors/', default='default_instructor.jpg')

    def __str__(self):
        return self.name

class Course(models.Model):
    image = models.ImageField(upload_to='course_images/')
    title = models.CharField(max_length=200)
    framework = models.CharField(max_length=200)
    read_more_slug = models.SlugField(unique=True, blank=True) 
    join_now_slug = models.SlugField(unique=True, blank=True)  
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    duration = models.CharField(max_length=50, default="0 hrs")
    students_enrolled = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.read_more_slug:
            self.read_more_slug = slugify(self.title + "-read-more")
        if not self.join_now_slug:
            self.join_now_slug = slugify(self.title + "-join-now")
        super().save(*args, **kwargs)
    
class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', default=1)
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    emergency_contact_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    emergency_phone_number = models.CharField(max_length=15)
    course_title = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_framework = models.CharField(max_length=100, blank=False, null=True)
    start_date = models.DateField()
    highest_education = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    EMPLOYMENT_STATUS_CHOICES = [
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('self_employed', 'Self-employed'),
        ('other', 'Other'),
    ]    
    employment_status = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES, blank=False) 
    employer_details = models.TextField()
    hear_about_course = models.CharField(max_length=200)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course_title}"


# Review Model
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    rating = models.PositiveIntegerField()  
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.course.title}"


# Video Model
class Video(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos', null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    youtube_id = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title


# Related Video Model
class RelatedVideo(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='related_videos', null=True)
    thumbnail = models.ImageField()
    description = models.TextField()
    thumbnail_url = models.URLField()
    title = models.CharField(max_length=200)
    video_url = models.URLField()

    def __str__(self):
        return self.title