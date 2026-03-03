from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    Usser Registration form. validate username and password
    """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
        )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
        )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
    def clean_username(self):
        username = self.cleaned_data.get('username').strip().lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        return email
        
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    
class UserLoginForm(AuthenticationForm):
    """
    User login form using Django built-in AuthenticationForm
    """
    
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your username',
                'autocomplete': 'username',
                'autofocus': True}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "autocomplete": "password"}
        ),
    )

    error_messages = {
        "invalid_login": "Incorrect username or password. Please try again.",
        "inactive": "This account has been disabled.",
    }
    
    class Meta:
        model = User
        fields = ['username', 'password']