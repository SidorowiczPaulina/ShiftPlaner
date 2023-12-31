from django.core.exceptions import ValidationError
from django.utils import timezone
from .constants import SHIFT_CHOICES
from django import forms
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_hours_limit = models.PositiveIntegerField()
    availability = models.ManyToManyField('viewer.UserAvailability')

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'viewer'


class Shift(models.Model):
    SHIFT_CHOICES = [
        ('First_Shift', '8:00-16:00'),
        ('Second_Shift', '14:00-22:00'),
    ]
    shift_id = models.AutoField(primary_key=True)
    shift_name = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    hours = models.IntegerField(default=8)
    min_num_workers = models.PositiveIntegerField(default=2)
    max_num_workers = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"Shift {self.shift_id}"


class UserAvailability(models.Model):
    user_availability_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.DateField(blank=True)
    shift_preferences = models.CharField(max_length=20, choices=SHIFT_CHOICES)

    def __str__(self):
        return f"{self.user_id.username}'s Availability"

    def clean(self):
        if self.day < timezone.now().date():
            raise ValidationError("Data nie może być z przeszłości.")


class WorkRestrictions(models.Model):
    work_restriction_id = models.AutoField(primary_key=True)
    max_daily_hours = models.PositiveIntegerField(8)
    min_hours_between = models.PositiveIntegerField(12)
    hours_limit = models.PositiveIntegerField(8)

    def __str__(self):
        return f"Work Restrictions {self.work_restriction_id}"


class Schedule(models.Model):
    UniqueID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shift_id = models.ForeignKey(Shift, on_delete=models.CASCADE)
    work_date = models.DateField()
    month = models.IntegerField(default=0)  # Domyślna wartość
    year = models.IntegerField(default=0)  # Domyślna wartość

    def __str__(self):
        return f"Schedule {self.UniqueID}"


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['user', 'work_date', 'month', 'year']
        widgets = {
            'user': forms.Select(attrs={'id': 'unique_id_user'}),
            'work_date': forms.DateInput(attrs={'id': 'unique_id_work_date', 'type': 'date'}),
        }

    def save(self, commit=True):
        if not self.instance.user.is_staff:
            self.instance.user = get_special_user()

        return super(ScheduleForm, self).save(commit)
