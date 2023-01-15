from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView


class CustomLoginView(LoginView):
    def get_form_class(self):
        # Gọi phương thức get_form_class() của lớp cha
        form_class = super().get_form_class()
        # Xóa label của tất cả các trường trong form
        for field in form_class.base_fields:
            form_class.base_fields[field].label = ""
        form_class.base_fields['username'].widget.attrs['placeholder'] = "Username"
        form_class.base_fields['password'].widget.attrs['placeholder'] = "Password"
        return form_class
    
class CustomRegister(UserCreationForm):
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super(CustomRegister, self).__init__(*args, **kwargs)       
        self.fields['username'].widget.attrs['placeholder'] = "Username"
        self.fields['password1'].widget.attrs['placeholder'] = "Password"
        self.fields['password2'].widget.attrs['placeholder'] = "Confirm Password"
        self.fields['email'].widget.attrs['placeholder'] = "Email"
        
    class Meta:
        model = User
        fields = ('username', 'email')
        
class CustomUpdateView(UpdateView):
    def get_form_class(self):
        # Gọi phương thức get_form_class() của lớp cha
        form_class = super().get_form_class()
        # Xóa label của tất cả các trường trong form
        for field in form_class.base_fields:
            form_class.base_fields[field].label = ""
        form_class.base_fields['complete'].label = "Complete?"
        form_class.base_fields['title'].widget.attrs['placeholder'] = "Title"
        form_class.base_fields['description'].widget.attrs['placeholder'] = "Description"
        return form_class
       
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != self.request.user:
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.cleaned_data['title'] = form.cleaned_data['title'].title()
        form.cleaned_data['description'] = form.cleaned_data['description'].title()
        form.cleaned_data['title'] = form.cleaned_data['title'].lower()
        form.cleaned_data['description'] = form.cleaned_data['description'].lower()
        return super().form_valid(form)
    
class CustomCreateView(CreateView):
    def get_form_class(self):
        # Gọi phương thức get_form_class() của lớp cha
        form_class = super().get_form_class()
        # Xóa label của tất cả các trường trong form
        for field in form_class.base_fields:
            form_class.base_fields[field].label = ""
        form_class.base_fields['title'].widget.attrs['placeholder'] = "Title"
        form_class.base_fields['description'].widget.attrs['placeholder'] = "Description"
        return form_class
    
    def form_valid(self, form):
        form.cleaned_data['title'] = form.cleaned_data['title'].title()
        form.cleaned_data['description'] = form.cleaned_data['description'].title()
        form.cleaned_data['title'] = form.cleaned_data['title'].lower()
        form.cleaned_data['description'] = form.cleaned_data['description'].lower()
        return super().form_valid(form)
        