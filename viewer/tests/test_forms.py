from django.contrib.auth.models import User
from django.test import TestCase

from ..forms import ScheduleForm


class ScheduleFormTestCase(TestCase):
    def test_schedule_form_valid_data(self):
        user = User.objects.create(username='testuser', password='testpassword')

        form_data = {
            'user': user,  # przekaż obiekt użytkownika
            'work_date': '2023-01-01',
            'month': 1,
            'year': 2023,
        }
        form = ScheduleForm(data=form_data)
        self.assertTrue(form.is_valid())
