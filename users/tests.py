from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import User
import datetime

class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.manager = User.objects.create(
            first_name="Manager",
            last_name="User",
            email="manager@example.com",
            role="manager",
            password=make_password("managerpassword")
        )

        self.employee = User.objects.create(
            first_name="Employee",
            last_name="User",
            email="employee@example.com",
            role="employee",
            password=make_password("employeepassword")
        )

    def test_login_view(self):
        # Success - Manager
        response = self.client.post(reverse('users:login'), {
            'email': 'manager@example.com',
            'password': 'managerpassword'
        })
        self.assertRedirects(response, reverse('tasks:manager_tasks'))

        # Success - Employee
        response = self.client.post(reverse('users:login'), {
            'email': 'employee@example.com',
            'password': 'employeepassword'
        })
        self.assertRedirects(response, reverse('tasks:employee_tasks'))

        # Invalid password
        response = self.client.post(reverse('users:login'), {
            'email': 'manager@example.com',
            'password': 'wrong'
        })
        self.assertContains(response, "Invalid password")

        # User not found
        response = self.client.post(reverse('users:login'), {
            'email': 'nouser@example.com',
            'password': 'password'
        })
        self.assertContains(response, "User not found")

    def test_register_view(self):
        # Success
        response = self.client.post(reverse('users:register'), {
            'first_name': 'Ali',
            'last_name': 'Saleh',
            'email': 'ali@example.com',
            'phone_number': '0100000000',
            'birthday': '2000-01-01',
            'role': 'employee',
            'category': 'Backend',
            'password': 'pass1234',
            'confirm_password': 'pass1234',
        })
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(email='ali@example.com').exists())

        # Passwords don't match
        response = self.client.post(reverse('users:register'), {
            'first_name': 'Samir',
            'last_name': 'Said',
            'email': 'samir@example.com',
            'phone_number': '0111111111',
            'birthday': '2001-02-02',
            'role': 'employee',
            'category': 'DevOps',
            'password': 'pass1234',
            'confirm_password': 'diff1234',
        })
        self.assertContains(response, 'Passwords do not match')

        # Email exists
        response = self.client.post(reverse('users:register'), {
            'first_name': 'Copy',
            'last_name': 'User',
            'email': 'manager@example.com',
            'phone_number': '0123456789',
            'birthday': '1980-12-12',
            'role': 'manager',
            'category': 'Frontend',
            'password': 'pass1234',
            'confirm_password': 'pass1234',
        })
        self.assertContains(response, 'Email already exists')

    def test_change_password_view(self):
        # Login first
        session = self.client.session
        session['user_id'] = self.manager.id
        session.save()

        # Wrong old password
        response = self.client.post(reverse('users:change_password'), {
            'old_password': 'wrong',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        self.assertContains(response, 'Old password is incorrect.')

        # Passwords don’t match
        response = self.client.post(reverse('users:change_password'), {
            'old_password': 'managerpassword',
            'new_password': 'abc123',
            'confirm_password': 'different'
        })
        self.assertContains(response, 'New passwords do not match.')

        # Success
        response = self.client.post(reverse('users:change_password'), {
            'old_password': 'managerpassword',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        self.assertRedirects(response, reverse('users:login'))

    def test_send_otp_view(self):
        # Existing email
        response = self.client.post(reverse('users:send_otp'), {
            'email': 'employee@example.com'
        })
        self.assertRedirects(response, reverse('users:verify_otp'))
        user = User.objects.get(email='employee@example.com')
        self.assertIsNotNone(user.reset_otp)

        # Non-existent email
        response = self.client.post(reverse('users:send_otp'), {
            'email': 'notfound@example.com'
        }, follow=True)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Email not found.')

    def test_verify_otp_view(self):
        # Set OTP manually
        self.employee.reset_otp = '123456'
        self.employee.otp_expiry = timezone.now() + datetime.timedelta(minutes=5)
        self.employee.save()

        # Correct OTP
        response = self.client.post(reverse('users:verify_otp'), {
            'email': 'employee@example.com',
            'otp': '123456'
        })
        self.assertRedirects(response, reverse('users:reset_password'))

        # Expired OTP
        self.employee.otp_expiry = timezone.now() - datetime.timedelta(minutes=1)
        self.employee.save()
        response = self.client.post(reverse('users:verify_otp'), {
            'email': 'employee@example.com',
            'otp': '123456'
        })
        self.assertRedirects(response, reverse('users:send_otp'))

        # Invalid OTP
        response = self.client.post(reverse('users:verify_otp'), {
            'email': 'employee@example.com',
            'otp': '000000'
        })
        self.assertContains(response, 'Invalid OTP.')

    def test_reset_password_view(self):
        # Set session and user
        self.employee.reset_otp = '654321'
        self.employee.otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        self.employee.save()
        session = self.client.session
        session['reset_user_id'] = self.employee.id
        session.save()

        # Password mismatch
        response = self.client.post(reverse('users:reset_password'), {
            'new_password': 'new123',
            'confirm_password': 'wrong'
        })
        self.assertRedirects(response, reverse('users:reset_password'))

        # Password match
        response = self.client.post(reverse('users:reset_password'), {
            'new_password': 'new123',
            'confirm_password': 'new123'
        })
        self.assertRedirects(response, reverse('users:login'))
        updated_user = User.objects.get(id=self.employee.id)
        self.assertIsNone(updated_user.reset_otp)
