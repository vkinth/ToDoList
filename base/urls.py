from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, TaskLogin, Register, MyDelete
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', TaskLogin.as_view() , name = "login"),
    path('register/', Register.as_view() , name = "register"),
    path('logout/', LogoutView.as_view(next_page="login") , name = "logout"),
    path('', TaskList.as_view() , name = "tasks"),   
    path('task/<int:pk>/', TaskDetail.as_view(), name="task"),
    path('create-task/' , TaskCreate.as_view(), name='task_create'),
    path('update-task/<int:pk>/' , TaskUpdate.as_view(), name='task_update'),
    path('delete-task/<int:pk>/' , MyDelete.delete, name='task_delete'),
]