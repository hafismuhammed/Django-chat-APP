from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from .forms import UserRegistrationForm, UserLoginForm


User = get_user_model()

class RedirectAuthenticatedMixin:
    """
    Mixin to redirect already login users to Chat App
    """
    redirect_url = reverse_lazy('user_list')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
    

class UserRegisterView(RedirectAuthenticatedMixin, CreateView):
    """
    View for user registration
    """
    
    model = User
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful! You can now log in.')
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please correct the errors below.")
        return super().form_invalid(form)
    

class UserLoginView(RedirectAuthenticatedMixin, LoginView):
    """
    View for the user login
    """
    template_name = 'login.html'
    form_class = UserLoginForm
    redirect_field_name = 'next'
    
    def get_default_redirect_url(self):
        return reverse_lazy('user_list')
    
    def form_valid(self, form):
        user = form.get_user()
        
        # Set the session expiry
        if not self.request.POST.get('remember'):
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(60 * 60 * 24 * 7)
            
        user.mark_online()
        login(self.request, user)
        # messages.success(self.request, f"Welcome back, {user.first_name}!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Login failed. Invalid Username or Password")
        return super().form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    """
    View for user logout. Redirects to login page.
    """
    
    login_url    = reverse_lazy("login")
    redirect_url = reverse_lazy("login")

    def post(self, request):
        if request.user.is_authenticated:
            request.user.mark_offline()
        logout(request)
        return redirect(self.redirect_url)

    def get(self, request):
        return redirect(self.redirect_url)

class UserListView(LoginRequiredMixin, ListView):
    """
    View for listing all users. Accessible only to logged-in users.
    """
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.exclude(
            username=self.request.user.username).filter(is_active=True)
