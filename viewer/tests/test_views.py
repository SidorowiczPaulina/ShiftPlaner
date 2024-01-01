from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse



class ScheduleViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_schedule_view_returns_302(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('generate_schedule'))
        self.assertEqual(response.status_code, 302)

    def test_schedule_view_requires_authentication(self):
        response = self.client.get(reverse('generate_schedule'))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_access_schedule_view(self):
        User.objects.create_user(username='admin', password='adminpassword', is_staff=True)
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('generate_schedule'))
        self.assertEqual(response.status_code, 200)

    def test_schedule_view_returns_valid_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('generate_schedule'))

        self.assertEqual(response.status_code, 302)
