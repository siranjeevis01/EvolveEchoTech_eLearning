from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, PasswordResetToken, Instructor, Course, Enrollment, Video, Review

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

admin.site.register(PasswordResetToken)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Instructor)
admin.site.register(Video)
admin.site.register(Review)
