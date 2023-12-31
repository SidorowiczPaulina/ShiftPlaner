from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import SHIFT_CHOICES, UserAvailability, Shift


class YourModelTestCase(TestCase):
    def test_user_availability_past_date(self):
        user = User.objects.create(username='testuser', password='testpassword')
        past_date = timezone.now() - timedelta(days=7)
        user_availability = UserAvailability(user_id=user, day=past_date, shift_preferences=SHIFT_CHOICES[0][0])

        with self.assertRaises(ValidationError):
            user_availability.full_clean()


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


class UserAvailabilityTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.shift = Shift.objects.create(shift_name='First_Shift', hours=8, min_num_workers=2, max_num_workers=3)

    def test_min_hours_between_shifts_valid(self):
        # Utwórz pierwszą dostępność
        user_availability_1 = UserAvailability.objects.create(user_id=self.user, day='2023-01-01', shift_preferences='First_Shift')

        # Utwórz drugą dostępność z odstępem czasowym większym niż minimalny (na przykład, 24 godziny)
        future_date = datetime.now() + timedelta(days=1)
        future_date_str = future_date.strftime('%Y-%m-%d')
        user_availability_2 = UserAvailability.objects.create(user_id=self.user, day=future_date_str, shift_preferences='First_Shift')

        # Oczekujemy, że nie będzie żadnego błędu walidacji
        user_availability_2.full_clean()

    def test_min_hours_between_shifts_invalid(self):
        # Utwórz pierwszą dostępność
        user_availability_1 = UserAvailability.objects.create(user_id=self.user, day='2023-01-01', shift_preferences='First_Shift')

        # Utwórz drugą dostępność z odstępem czasowym mniejszym niż minimalny (na przykład, 8 godzin)
        user_availability_2 = UserAvailability.objects.create(user_id=self.user, day='2023-01-01', shift_preferences='First_Shift')

        # Oczekujemy, że podczas walidacji zostanie podniesiony błąd
        with self.assertRaises(ValidationError):
            user_availability_2.full_clean()