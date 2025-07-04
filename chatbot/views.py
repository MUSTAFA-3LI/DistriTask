from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Task
from users.models import User
from django.utils import timezone
from django.db.models import Count ,Q
from .serializers import UserSerializer
from .serializers import TaskSerializer


#return count of all system tasks
@api_view(['GET'])
def total_tasks(request):
    count = Task.objects.all().count()
    return Response({"answer": f"There are {count} total tasks."})

#return count of completed tasks
@api_view(['GET'])
def completed_tasks(request):
    count = Task.objects.filter(status='completed').count()
    return Response({"answer": f"There are {count} completed tasks."})

# delayed Tasks
@api_view(['GET'])
def overdue_tasks(request):
    today = timezone.now().date()
    count = Task.objects.filter(deadline__lt=today).exclude(status='completed').count()
    return Response({"answer": f"There are {count} overdue tasks."})

#return count of delayed tasks
@api_view(['GET'])
def delayed_tasks(request):
    today = timezone.now().date()
    count = Task.objects.filter(deadline__lt=today).exclude(
        status='completed').count()
    return Response({"answer": f"There are {count} delayed tasks."})


#get top 3 employees
@api_view(['GET'])
def top_employees(request):
    top = (
        User.objects.annotate(
            completed=Count('assigned_tasks', filter=Q(assigned_tasks__status='completed'))
        )
        .order_by('-completed')[:3]
    )

    if not top:
        return Response({"answer": "No task completion data available."})

    message = "Top 3 employees by completed tasks:\n"
    for i, user in enumerate(top, 1):
        message += f"{i}. {user.first_name} {user.last_name} – {user.completed} tasks\n"
    return Response({"answer": message.strip()})

#Completion Percentage
@api_view(['GET'])
def completion_rate(request):
    total = Task.objects.count()
    completed = Task.objects.filter(status='completed').count()
    if total == 0:
        return Response({"answer": "There are no tasks in the system."})
    percent = (completed / total) * 100
    return Response({"answer": f"{percent:.2f}% of tasks are completed."})

#tasks_due_on_date
@api_view(['GET'])
def tasks_due_on_date(request):
    date_str = request.GET.get('date')  # format YYYY-MM-DD
    try:
        due_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return Response({"answer": "Please provide a valid date in YYYY-MM-DD format."})

    tasks = Task.objects.filter(due_date=due_date)
    if not tasks:
        return Response({"answer": f"No tasks are due on {due_date}."})

    message = f"Tasks due on {due_date}:\n"
    for task in tasks:
        message += f"- {task.title}\n"
    return Response({"answer": message.strip()})

#task per category 
@api_view(['GET'])
def tasks_per_category(request, category_name):
    count = Task.objects.filter(category__iexact=category_name).count()

    if count == 0:
        return Response({"answer": f"No tasks found in category '{category_name}'."})
    
    return Response({"answer": f"There are {count} tasks in the '{category_name}' category."})

#Get task ID Using Task Name
@api_view(['GET'])
def task_id(request, Task_Name):
    task = Task.objects.filter(title__iexact=Task_Name).first()

    if task :
        return Response({"answer": f"ID is '{task.id}'."})
    
    return Response({"answer": f"There are no task with this titls"})

#task count for each user
@api_view(['GET'])
def tasks_for_user(request, username):
    users = User.objects.filter(first_name__iexact=username)
    
    if not users.exists():
        return Response({"answer": f"No user found with the first name '{username}'."})

    total_tasks = 0
    multiUserInfo = []

    for user in users:
        count = Task.objects.filter(assigned_to=user).count()
        total_tasks += count
        multiUserInfo.append(f"{user.first_name}: {count} task(s)")

    if len(users) == 1:
        return Response({"answer": f"{username.capitalize()} has {total_tasks} task(s) assigned."})
    else:
        details = "\n".join(multiUserInfo)
        return Response({
            "answer": f"Multiple users found with name '{username}':\n{details}"
        })

#show user informations
@api_view(['GET'])
def user_info (request , username):
    users = User.objects.filter(first_name__iexact=username)
    
    if not users.exists():
        return Response({"answer": f"No user found with the first name '{username}'."})

    user = users.first()
    message = (
        f"User Info:\n"
        f" Name: {user.first_name} {user.last_name}\n"
        f"Email: {user.email}\n"
        f"Department: {user.category}\n"
        f"birthday: {user.birthday}\n"
        f"phone number: {user.phone_number}\n"
    )

    return Response({"answer": message})
    # serializer = UserSerializer(user)
    # return Response(serializer.data)


#change task assignment to employees
@api_view(['POST' , 'GET'])
def reassign_user (request , task_num , new_user):
    try:
        task = Task.objects.get(pk=task_num)
    except Task.DoesNotExist:
        return Response({
            "answer": f"No task found with number: '{task_num}'"
        }, status=404)
    
    users= User.objects.filter(first_name__iexact=new_user)
    if not users.exists():
        return Response ({'answer' : f'no user found with name {new_user}'} , status=404)
    
    user = users.first()   #incase multible users choice first one
    task.assigned_to = user
    task.save()
    return Response({
        "answer": f"Task '{task.title}' is now assigned to {user.first_name} ({user.last_name})."
    })

                        