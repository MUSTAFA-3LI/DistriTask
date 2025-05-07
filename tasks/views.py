from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from users.models import User
from django.contrib import messages
from datetime import datetime
from django.db.models import Count
from django.db.models import Q

from django.core.mail import send_mail

from celery import shared_task
from .tasks import check_deadlines

from django.core.paginator import Paginator


# function to send emails to employees of  new tasks
def send_task_email(employee, task):
    subject = " New Task Assigned to You!"
    message = f"""
Hey {employee.first_name}, 

You've been assigned a new task!

 Title: {task.title}
 Description: {task.description}
 Priority: {task.priority}
 Deadline: {task.deadline}
 Category: {task.category}

Please log in to your dashboard to view more details and start working on it.

Distritask - Let the right task find the right talent."""

    send_mail(
        subject=subject,
        message=message,
        from_email='ahmed.h.ramadan.cs@email.com',
        recipient_list=[employee.email],
        fail_silently=True
    )

# View tasks of the logged-in employee


def employee_tasks(request):
    if request.session.get('user_role') != 'employee':
        return redirect('users:login')

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('users:login')

    tasks = Task.objects.filter(assigned_to_id=user_id)

    return render(request, 'tasks/employee_tasks.html', {'tasks': tasks})

# Add a new task (Manager only)


def add_task(request):
    if request.session.get('user_role') != 'manager':
        return redirect('users:login')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority = request.POST.get('priority', 'medium')
        deadline = request.POST.get('deadline')
        category = request.POST.get('category', '').strip()

        # Ensure category is provided
        if not category:
            messages.error(request, "Category is required.")
            return redirect('tasks:manager_tasks')

        # Find an available employee in the same category
        suitable_employee = User.objects.filter(role='employee', category=category) \
                                        .annotate(task_count=Count('task', filter=~Q(task__status='completed'))) \
                                        .order_by('task_count') \
                                        .first()

        if not suitable_employee:
            messages.error(request, "No available employees in this category.")
            return redirect('tasks:manager_tasks')

        # Create the task and assign it to the employee
        task = Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
            category=category,
            assigned_to=suitable_employee
        )
        messages.success(request, "Task added successfully.")

        # Send task assignment email
        send_task_email(suitable_employee, task)

        return redirect('tasks:manager_tasks')

    return redirect('tasks:manager_tasks')


# manager update task
def update_task(request, task_id):
    if request.session.get('user_role') != 'manager':
        return redirect('users:login')

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        deadline = request.POST.get('deadline')

        if title:
            task.title = title
        if description:
            task.description = description
        if priority in ['low', 'medium', 'high', 'urgent']:
            task.priority = priority
        if status in ['pending', 'in_progress', 'completed', 'delayed']:
            task.status = status
        if deadline:
            task.deadline = deadline

        task.save()
        messages.success(request, "Task updated successfully.")
        return redirect('tasks:manager_tasks')

    return redirect('tasks:manager_tasks')

# Update task status (Employee only)


def update_task_status(request, task_id):
    if request.session.get('user_role') != 'employee':
        return redirect('users:login')

    user_id = request.session.get('user_id')
    task = get_object_or_404(Task, id=task_id)

    if task.assigned_to.id != user_id:
        messages.error(request, "You can only update tasks assigned to you.")
        return redirect('tasks:employee_tasks')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'in_progress', 'completed', 'delayed']:
            task.status = new_status
            task.save()
            messages.success(request, "Task status updated successfully.")
        else:
            messages.error(request, "Invalid status update.")

    return redirect('tasks:employee_tasks')

# Delete a task (Manager only)


def delete_task(request, task_id):
    if request.session.get('user_role') != 'manager':
        return redirect('users:login')

    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, "Task deleted successfully.")

    return redirect('tasks:manager_tasks')

# LOGOUT


def log_out(request):
    request.session.flush()
    return redirect("users:login")

# this function used in get employees in manger page and thier tasks


def manager_tasks(request):

    # check_deadlines.delay()

    # Check if the user is a manager; if not, redirect to the login page
    if request.session.get('user_role') != 'manager':
        return redirect('users:login')

    # Fetch all tasks from the database
    tasks = Task.objects.all()

    # Implement pagination
    paginator = Paginator(tasks, 6)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch unique categories from the Task model
    categories = User.objects.values_list(
        'category', flat=True).distinct()  # pass category to manager page

    # Fetch all employees (users with the role 'employee')
    employees = User.objects.filter(role='employee')

    # Create a list to store employee data
    employee_data = []

    # Loop through each employee to calculate task statistics
    for employee in employees:
        # Count total tasks assigned to the employee
        total_tasks = Task.objects.filter(assigned_to=employee).count()

        # Count delayed tasks assigned to the employee
        delayed_tasks = Task.objects.filter(
            assigned_to=employee, status='delayed').count()

        # Count completed tasks assigned to the employee
        completed_tasks = Task.objects.filter(
            assigned_to=employee, status='completed').count()

        # Add the employee's data to the list
        employee_data.append({
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'total_tasks': total_tasks,
            'delayed_tasks': delayed_tasks,
            'completed_tasks': completed_tasks,
        })

    # Pass the paginated tasks to the template
    return render(request, 'tasks/manager_tasks.html', {
        'page_obj': page_obj,
        'employees': employees,
        'employee_data': employee_data,  # Pass employee data to the template
        'categories': categories,
    })
