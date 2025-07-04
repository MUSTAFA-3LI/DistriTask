from django.urls import path
from .views_auth import CustomObtainAuthToken
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('total-tasks/', views.total_tasks, name='total_tasks'),  
    path('completed-tasks/', views.completed_tasks, name='completed_tasks'),
    path('delayed-tasks/', views.delayed_tasks, name='delayed_tasks'),
    path('top-employees/', views.top_employees, name='top_employees'),
    path('completion-rate/', views.completion_rate, name='completion_rate'),
    path('tasks-due-on/', views.tasks_due_on_date, name='tasks_due_on_date'),
    path('overdue-tasks/', views.overdue_tasks, name='overdue_tasks'),
    path('tasks-per-category/<str:category_name>/', views.tasks_per_category, name='tasks_per_category'),
    path('tasks-for-user/<str:username>/', views.tasks_for_user, name='tasks_for_user'),
    path('user-info/<str:username>/', views.user_info, name='user_info'),
    path('reassign-task/<int:task_num>/<str:new_user>/', views.reassign_user, name='reassign_user'),
    path('task-id/<str:Task_Name>/', views.task_id, name='task_id'),



    path('api-token-auth/', CustomObtainAuthToken.as_view()),


]
