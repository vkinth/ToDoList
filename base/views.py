from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import CustomLoginView, CustomRegister, CustomUpdateView, CustomCreateView
from .models import Task


class TaskLogin(CustomLoginView):
    template_name = "login.html"
    fields = '__all__'
    redirect_authenticated_user = True
    
    # Redirect user to task list after successful login
    def get_success_url(self):
        return reverse_lazy('tasks')
    
    
class Register(FormView, CustomRegister):
    template_name = "register.html"
    form_class = CustomRegister
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")
    
     # login user after successful registration
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)
    
    # redirect authenticated user to task list
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register, self).get(*args, **kwargs)
    
    
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "task_list"
    
    
    # filter tasks by user and add the count of incomplete tasks to the context
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['task_list'] = context['task_list'].filter(user=self.request.user)
        context['count'] = context['task_list'].filter(complete=False).count()
        return context    
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"
    
    
class TaskCreate(LoginRequiredMixin, CustomCreateView):
    model = Task
    template_name = "task_create.html"
    fields = ['title', 'description']
    success_url = reverse_lazy("tasks")
    
    # set the task's user to the current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin, CustomUpdateView):
    model = Task
    template_name = "task_form.html"
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy("tasks")
    

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name_suffix = None
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy('tasks')
    
class MyDelete(LoginRequiredMixin):
    # check authentication and user's ownership before deleting task
    def delete(request, pk):
        if request.user.is_authenticated:
            task_ids = Task.objects.filter(user=request.user).values_list('id', flat=True)
            if pk in task_ids:
                Task.objects.get(id=pk).delete()
                return HttpResponseRedirect(reverse_lazy("tasks"))
            return HttpResponseRedirect(reverse_lazy("tasks"))
        else:
            return HttpResponseRedirect(reverse_lazy("login"))

    