from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from chat.models import Message

class ChatViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # إنشاء المستخدمين
        self.manager = User.objects.create_user(
            email='manager@test.com', password='testpass123', role='manager',
            first_name='Manager', last_name='User'
        )
        self.employee = User.objects.create_user(
            email='employee@test.com', password='testpass123', role='employee',
            first_name='Employee', last_name='User'
        )

        # تسجيل دخول المدير
        self.client.login(email='manager@test.com', password='testpass123')

    def test_chat_page_view(self):
        response = self.client.get(reverse('chat:chat_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('employees', response.context)

    def test_employee_chat_page_view(self):
        self.client.logout()
        self.client.login(email='employee@test.com', password='testpass123')
        response = self.client.get(reverse('chat:employee_chat'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'chat')  # بدل room_name
        self.assertContains(response, self.manager.email)  # تأكيد وجود المدير في الصفحة

    def test_manager_private_chat_view(self):
        url = reverse('chat:manager_private_chat', args=[self.employee.email])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.employee.email)

    def test_message_list_view(self):
        # إنشاء رسالة
        Message.objects.create(sender=self.employee, receiver=self.manager, content='Hello')
        room_name = f"{min(self.manager.email, self.employee.email)}__{max(self.manager.email, self.employee.email)}"
        response = self.client.get(reverse('chat:chat_messages') + f'?room={room_name}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_mark_read_view(self):
        Message.objects.create(sender=self.employee, receiver=self.manager, content='Hi', is_read=False)
        response = self.client.get(reverse('chat:mark_read') + f'?email={self.employee.email}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')
        self.assertTrue(Message.objects.filter(sender=self.employee, receiver=self.manager).first().is_read)

    def test_unread_counts_view(self):
        Message.objects.create(sender=self.employee, receiver=self.manager, content='Unread', is_read=False)
        response = self.client.get(reverse('chat:unread_counts'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.employee.email, response.json())

    def test_unread_counts_unauthorized(self):
        self.client.logout()
        self.client.login(email='employee@test.com', password='testpass123')
        response = self.client.get(reverse('chat:unread_counts'))
        self.assertEqual(response.status_code, 403)

