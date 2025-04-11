from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, Enrollment, Review
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        if len(password) < 6 or len(password) > 14:
            raise ValidationError("Password must be between 6 and 14 characters long")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number")
        if not any(char in '@$!%*?&' for char in password):
            raise ValidationError("Password must contain at least one special character (@$!%*?&)")
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        
        if CustomUser.objects.filter(username=username).exists():
            self.add_error('username', "Username already exists")

class SignInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password'
        })
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)

class ContactForm(forms.ModelForm):
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control col-12', 'placeholder': 'Subject', 'required': 'required'}),
        required=True
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control col-12', 'rows': 5, 'placeholder': 'Message', 'required': 'required'}),
        required=True
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def send_email(self):
        send_mail(
            self.cleaned_data['subject'],
            self.cleaned_data['message'],
            self.cleaned_data['email'],
            ['siranjeevicad01@gmail.com'],
            fail_silently=False,
        )

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']