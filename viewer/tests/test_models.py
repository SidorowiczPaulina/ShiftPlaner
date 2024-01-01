from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ..models import SHIFT_CHOICES, UserAvailability, Shift


class YourModelTestCase(TestCase):
    def test_user_availability_past_date(self):
        user = User.objects.create(username='testuser', password='testpassword')
        past_date = timezone.now() - timedelta(days=7)
        user_availability = UserAvailability(user_id=user, day=past_date, shift_preferences=SHIFT_CHOICES[0][0])

        with self.assertRaises(ValidationError):
            user_availability.full_clean()

    def test_min_hours_between_shifts(self):
        future_date = timezone.now() + timedelta(days=1)
        future_date_str = future_date.strftime('%Y-%m-%d')
        user = User.objects.create_user(username='testuser', password='testpassword')
        shift = Shift.objects.create(shift_name='First_Shift', hours=8, min_num_workers=2, max_num_workers=3)

        user_availability_1 = UserAvailability.objects.create(user_id=user, day=future_date_str,
                                                              shift_preferences='First_Shift')

        try:
            user_availability_1.full_clean()
        except ValidationError as e:
            self.fail(f"test_min_hours_between_shifts failed with ValidationError: {e}")

        user_availability_2 = UserAvailability.objects.create(user_id=user, day='2023-01-01',
                                                              shift_preferences='First_Shift')

        with self.assertRaises(ValidationError):
            user_availability_2.full_clean()


class UserAvailabilityTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.shift = Shift.objects.create(shift_name='First_Shift', hours=8, min_num_workers=2, max_num_workers=3)

    def test_min_hours_between_shifts(self):

        future_date = timezone.now() + timedelta(days=1)
        future_date_str = future_date.strftime('%Y-%m-%d')
        user_availability_1 = UserAvailability.objects.create(user_id=self.user, day=future_date_str,
                                                              shift_preferences='First_Shift')

        try:
            user_availability_1.full_clean()
        except ValidationError as e:
            self.fail(f"test_min_hours_between_shifts failed with ValidationError: {e}")

        user_availability_2 = UserAvailability.objects.create(user_id=self.user, day='2023-01-01',
                                                              shift_preferences='First_Shift')

        with self.assertRaises(ValidationError):
            user_availability_2.full_clean()
