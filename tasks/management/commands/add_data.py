from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from tasks.models import User, Task
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'add the database with users and project-related tasks'

    def handle(self, *args, **kwargs):
        Task.objects.all().delete()
        # Define users
        users_data = [
            {
                'first_name': 'Ahmed',
                'last_name': 'Hamdy',
                'email': 'oreof00024@gmail.com',
                'password': '12345',
                'role': 'employee',
                'category': 'Backend',
            },
            {
                'first_name': 'Yoused',
                'last_name': 'Mostafa',
                'email': 'youssifmostafa192@gmail.com',
                'password': '12345',
                'role': 'employee',
                'category': 'Frontend',
            },
            {
                'first_name': 'Mustafa',
                'last_name': 'Ali',
                'email': 'mustafa09402@gmail.com',
                'password': '12345',
                'role': 'employee',
                'category': 'DevOps',
            },
            {
                'first_name': 'Emad',
                'last_name': 'Kamal',
                'email': 'emadbadr227@gmail.com',
                'password': '12345',
                'role': 'employee',
                'category': 'Backend',
            },
            {
                'first_name': 'Ahmed',
                'last_name': 'Hamdy',
                'email': 'ahmedhandy06@gmail.com',
                'password': '12345',
                'role': 'manager',
                'category': '',
            },
        ]

        user_objects = {}

        for data in users_data:
            user, _ = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': data['role'],
                    'category': data['category'],
                    'password': make_password(data['password']),
                    'birthday': timezone.now().date(),
                }
            )
            user_objects[data['email']] = user
            self.stdout.write(self.style.SUCCESS(f"Created/Found user {user.email}"))

        # Define tasks
        tasks_data = [
            # Ahmed's tasks
            {
                'title': 'Implement Manager Dashboard View',
                'description': 'Create a backend view to display manager-specific data and analytics.',
                'assigned_to': user_objects['oreof00024@gmail.com'],
            },
            {
                'title': 'User Authentication Logic',
                'description': 'Develop login and registration mechanisms.',
                'assigned_to': user_objects['oreof00024@gmail.com'],
            },
            {
                'title': 'Password Reset via OTP & Password Change',
                'description': 'Implement backend logic to send OTP to email for password reset, verify OTP, and allow users to set a new password.',
                'assigned_to': user_objects['oreof00024@gmail.com'],
            },
            {
                'title': 'Task Category Model',
                'description': 'Create a model to define task categories and use them in task creation and filtering.',
                'assigned_to': user_objects['oreof00024@gmail.com'],
            },
            {
                'title': 'Task Assignment Algorithm',
                'description': 'Implement logic to assign tasks to employees based on category and least number of uncompleted tasks.',
                'assigned_to': user_objects['oreof00024@gmail.com'],
            },
            {
            'title': 'Send Task Details via Email',
            'description': 'An email sent to employees with the assigned task details.',
            'assigned_to': user_objects['oreof00024@gmail.com'],
            },
            {
                'title': 'Implement Celery for Periodic Task Status Checks',
                'description': 'Set up Celery with Django to run periodic tasks that check and update the status of ongoing tasks regulary.',
                'assigned_to': user_objects['oreof00024@gmail.com'],
            },

            # Emad's tasks
            {
                'title': 'Implement Employee Task View',
                'description': 'Develop a secure view that displays tasks specific to the logged-in employee.',
                'assigned_to': user_objects['emadbadr227@gmail.com'],
            },
            {
                'title': 'Write Unit Tests for User and Task Models',
                'description': 'Create unit tests for user creation, task-user linking, and employee task view logic.',
                'assigned_to': user_objects['emadbadr227@gmail.com'],
            },
            {
                'title': 'Setup Test Data for Employees and Tasks',
                'description': 'Insert sample users and tasks to test proper distribution of tasks among employees.',
                'assigned_to': user_objects['emadbadr227@gmail.com'],
            },
            {
                'title': 'Integrate Django Flash Messages',
                'description': 'Implement success messages for task operations and user login/logout actions.',
                'assigned_to': user_objects['emadbadr227@gmail.com'],
            },
            {
                'title': 'Add Employee Analytics to Manager Dashboard',
                'description': 'Display total employees and task summaries to visualize workload per employee.',
                'assigned_to': user_objects['emadbadr227@gmail.com'],
            },

            # Yoused's tasks
            {
                'title': 'Design Task View Page (Frontend)',
                'description': 'Create a styled, responsive UI for task display for users.',
                'assigned_to': user_objects['youssifmostafa192@gmail.com'],
            },
            {
            'title': 'Design Dashboard Layout',
            'description': 'Create a responsive and user-friendly layout for the admin and user dashboards.',
            'assigned_to': user_objects['youssifmostafa192@gmail.com'],
            },
            {
                'title': 'Implement Authentication UI',
                'description': 'Develop the frontend pages for login, registration, and password reset with proper validations.',
                'assigned_to': user_objects['youssifmostafa192@gmail.com'],
            },
            {
                'title': 'Build Static Task Display Pages',
                'description': 'Create static pages to display task data, placeholders for dynamic content.',
                'assigned_to': user_objects['youssifmostafa192@gmail.com'],
            },
            {
                'title': 'Add Styling and Hover Effects',
                'description': 'Apply consistent dark theme styling and add hover animations to enhance user experience.',
                'assigned_to': user_objects['youssifmostafa192@gmail.com'],
            },

            # Mustafa's tasks
            {
            'title': 'Infrastructure Provisioning',
            'description': 'Provision cloud resources using IaC tools like Terraform.',
            'assigned_to': user_objects['mustafa09402@gmail.com'],
            },
            {
                'title': 'CI/CD Pipeline Setup',
                'description': 'Build automated pipelines for testing, building, and deployment.',
                'assigned_to': user_objects['mustafa09402@gmail.com'],
            },
            {
                'title': 'Configuration Management with Ansible',
                'description': 'Automate server configuration, software installation, and environment setup using Ansible playbooks and roles.',
                'assigned_to': user_objects['mustafa09402@gmail.com'],
            },
            {
                'title': 'Backup and Recovery',
                'description': 'Implement automated backups and disaster recovery plans.',
                'assigned_to': user_objects['mustafa09402@gmail.com'],
            },
            {
                'title': 'Security and Access Management',
                'description': 'Manage IAM roles and secure cloud access.',
                'assigned_to': user_objects['mustafa09402@gmail.com'],
            },
            {
                'title': 'Monitoring and Logging',
                'description': 'Set up tools for system monitoring and centralized logging.',
                'assigned_to': user_objects['mustafa09402@gmail.com'],
            },
            {
                'title': 'Kubernetes Deployment',
                'description': 'Deploy and manage apps on Kubernetes clusters.',
                'assigned_to': user_objects['mustafa09402@gmail.com'],
            },
            {
                'title': 'Dockerization',
                'description': 'Containerize apps using Docker and manage them with Docker Compose.',
                'assigned_to': user_objects['mustafa09402@gmail.com'],
            },
        ]

        priority_choices = ['low', 'medium', 'high']
        status_choices = ['pending', 'in_progress', 'completed']

        for task_data in tasks_data:
            created_at = timezone.now() - timedelta(days=random.randint(1, 10))
            deadline = created_at + timedelta(days=random.randint(10, 30))
            task = Task.objects.create(
                title=task_data['title'],
                description=task_data['description'],
                assigned_to=task_data['assigned_to'],
                created_at=created_at,
                deadline=deadline,
                priority=random.choice(priority_choices),
                status=random.choice(status_choices),
                category=task_data['assigned_to'].category
            )
            self.stdout.write(self.style.SUCCESS(f"Created task: {task.title} for {task.assigned_to.email}"))
