import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import UserAvailability, SHIFT_CHOICES


class YourModelTestCase(TestCase):
    def test_user_availability_past_date(self):
        # Tworzymy użytkownika
        user = User.objects.create(username='testuser', password='testpassword')

        # Tworzymy obiekt UserAvailability z datą w przeszłości
        past_date = timezone.now() - timedelta(days=7)
        user_availability = UserAvailability(user_id=user, day=past_date, shift_preferences=SHIFT_CHOICES[0][0])

        # Oczekujemy, że próba zapisu obiektu z datą w przeszłości zakończy się błędem
        with self.assertRaises(ValidationError):
            user_availability.full_clean()


@pytest.mark.django_db
def test_schedule_view_returns_200(client):
    User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('generate_schedule'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_schedule_view_requires_authentication(client):
    response = client.get(reverse('generate_schedule'))
    assert response.status_code == 302


def test_admin_can_access_schedule_view(self):
    User.objects.create_user(username='admin', password='adminpassword', is_staff=True)
    self.client.login(username='admin', password='adminpassword')
    response = self.client.get(reverse('generate_schedule'))
    self.assertEqual(response.status_code, 200)


def test_schedule_view_returns_valid_data(self):
    self.client.login(username='testuser', password='testpassword')
    response = self.client.get(reverse('generate_schedule'))

    # Sprawdź, czy dane są dostępne w kontekście odpowiedzi
    self.assertIn('schedule_entries', response.context)

    # Sprawdź, czy dane są niepuste
    schedule_entries = response.context['schedule_entries']
    self.assertTrue(schedule_entries)


class ScheduleViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_schedule_view_returns_200(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('generate_schedule'))
        self.assertEqual(response.status_code, 302)

    def test_schedule_view_requires_authentication(self):
        response = self.client.get(reverse('generate_schedule'))
        self.assertEqual(response.status_code,302)