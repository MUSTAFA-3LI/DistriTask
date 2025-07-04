from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from users.models import User
from .models import Task

class TaskViewsTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create(
            first_name="Manager",
            last_name="User",
            email="manager@example.com",
            role="manager",
            password="managerpassword",
            category="management"
        )

        self.employee = User.objects.create(
            first_name="Employee",
            last_name="User",
            email="employee@example.com",
            role="employee",
            password="employeepassword",
            category="development"
        )

        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            assigned_to=self.employee,
            status="completed",
            priority="medium",
            deadline=timezone.now() + timedelta(days=7),
            category="development"
        )

        self.client = Client()

    def _login_user(self, user):
        session = self.client.session
        session['user_id'] = user.id
        session['user_role'] = user.role
        session.save()

    def test_manager_tasks_view(self):
        self._login_user(self.manager)
        response = self.client.get(reverse('tasks:manager_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_employee_tasks_view(self):
        self._login_user(self.employee)
        response = self.client.get(reverse('tasks:employee_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_add_task_view(self):
        self._login_user(self.manager)
        data = {
            'title': 'New Task',
            'description': 'This is a new task',
            'priority': 'high',
            'deadline': (timezone.now() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M'),
            'category': 'development'
        }
        response = self.client.post(reverse('tasks:add_task'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_update_task_status_view(self):
        self._login_user(self.employee)
        data = {'status': 'completed'}
        response = self.client.post(reverse('tasks:update_task_status', args=[self.task.id]), data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')

    def test_delete_task_view(self):
        self._login_user(self.manager)
        response = self.client.post(reverse('tasks:delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_logout_view(self):
        self._login_user(self.manager)
        response = self.client.get(reverse('tasks:log_out'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('user_id', self.client.session)

    def test_update_task_view(self):
        self._login_user(self.manager)
        data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'priority': 'urgent',
            'status': 'in_progress',
            'deadline': (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M')
        }
        response = self.client.post(reverse('tasks:update_task', args=[self.task.id]), data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'in_progress')
