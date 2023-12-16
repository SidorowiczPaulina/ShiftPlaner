from django.test import TestCase
from django.contrib.auth.models import User
from datetime import timedelta
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