from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from . import models
from .forms import ScheduleForm
from .forms import UserAvailabilityForm
from .models import UserAvailability, Shift, Schedule, WorkRestrictions
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware
from django.db import models
from django.db.models import Sum
from calendar import monthrange
from datetime import date, timedelta
from datetime import date, timedelta
from calendar import monthrange
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserAvailability, WorkRestrictions, Shift, Schedule  # Dodaj import dla modelu Schedule
from django.db import models
from .models import Schedule
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render, redirect
from datetime import timedelta
from .models import UserAvailability, WorkRestrictions, Shift, Schedule
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models
from django.utils import timezone
from django.shortcuts import render
from django.contrib import messages
from .models import UserAvailability, Schedule, Shift, WorkRestrictions
from datetime import date, timedelta
from calendar import monthrange
from django.db import models
from django.contrib.auth.decorators import user_passes_test

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('base')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('base')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('base')


def base(request):
    return render(request, "base.html")

def is_admin(user):
    return user.is_authenticated and user.is_staff

def enter_availability(request):
    if request.method == 'POST':
        form = UserAvailabilityForm(request.POST)
        if form.is_valid():
            user = request.user
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return redirect('availability_list')
    else:
        form = UserAvailabilityForm()
    return render(request, 'schedule/enter_availability.html', {'form': form})



def root(request):
    return render(request, 'root.html')




def availability_list(request):
    if request.user.is_staff:
        # Administrator widzi wszystkie dyspozycje użytkowników
        user_availabilities = UserAvailability.objects.all()
    else:
        # Zwykły użytkownik widzi tylko swoje dyspozycje
        user_availabilities = UserAvailability.objects.filter(user_id=request.user)

    context = {
        'user_availabilities': user_availabilities,
    }

    return render(request, 'schedule/availability_list.html', context)

@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def schedule_list(request):


    schedule = Schedule.objects.all()

    return render(request, "schedule/schedule_list.html", {'schedule': schedule})

    if created:
        messages.info(request, "Work restrictions created successfully.")

    # Tworzenie obiektów Shift, jeśli nie istnieją
    shifts_data = [
        {'shift_name': 'First_Shift', 'hours': 8, 'min_num_workers': 2, 'max_num_workers': 3},
        {'shift_name': 'Second_Shift', 'hours': 8, 'min_num_workers': 2, 'max_num_workers': 3},
        # Dodaj inne zmienne zmienne według potrzeb
    ]

    for shift_data in shifts_data:
        shift, created = Shift.objects.get_or_create(
            shift_name=shift_data['shift_name'],
            defaults={
                'hours': shift_data['hours'],
                'min_num_workers': shift_data['min_num_workers'],
                'max_num_workers': shift_data['max_num_workers']
            }
        )

        if created:
            messages.info(request, f"Shift {shift.shift_name} created successfully.")


    users_availabilities = UserAvailability.objects.all()

    schedule_entries = []

    for user_availability in users_availabilities:
        try:
            shift = Shift.objects.get(shift_name=user_availability.shift_preferences)
        except Shift.DoesNotExist:
            messages.error(request, f"Shift {user_availability.shift_preferences} does not exist.")
            continue

        existing_hours_for_user = Schedule.objects.filter(
            user=user_availability.user_id,
            work_date=user_availability.day
        ).aggregate(models.Sum('shift_id__hours'))['shift_id__hours__sum'] or 0

        if existing_hours_for_user + shift.hours <= work_restrictions.max_daily_hours:
            min_hours_between_shifts = work_restrictions.min_hours_between

            if Schedule.objects.filter(
                    user=user_availability.user_id,
                    work_date__lt=user_availability.day,
                    work_date__gte=user_availability.day - timedelta(hours=min_hours_between_shifts)
            ).exists():
                continue

            schedule_entry = Schedule.objects.create(
                user=user_availability.user_id,
                shift_id=shift,
                work_date=user_availability.day
            )
            schedule_entries.append(schedule_entry)

    all_schedule_entries = Schedule.objects.all()

    return render(request, 'schedule/schedule_list.html', {'schedule_entries': all_schedule_entries})



@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def generate_schedule(request):
    # Tworzenie obiektu WorkRestrictions, jeśli nie istnieje
    work_restrictions, created = WorkRestrictions.objects.get_or_create(
        max_daily_hours=8,
        min_hours_between=12,
        hours_limit=8
    )

    if created:
        messages.info(request, "Work restrictions created successfully.")

    # Tworzenie obiektów Shift, jeśli nie istnieją
    shifts_data = [
        {'shift_name': 'First_Shift', 'hours': 8, 'min_num_workers': 2, 'max_num_workers': 3},
        {'shift_name': 'Second_Shift', 'hours': 8, 'min_num_workers': 2, 'max_num_workers': 3},

    ]

    for shift_data in shifts_data:
        shift, created = Shift.objects.get_or_create(
            shift_name=shift_data['shift_name'],
            defaults={
                'hours': shift_data['hours'],
                'min_num_workers': shift_data['min_num_workers'],
                'max_num_workers': shift_data['max_num_workers']
            }
        )

        if created:
            messages.info(request, f"Shift {shift.shift_name} created successfully.")


    users_availabilities = UserAvailability.objects.all()

    schedule_entries = []

    for user_availability in users_availabilities:
        try:
            shift = Shift.objects.get(shift_name=user_availability.shift_preferences)
        except Shift.DoesNotExist:
            messages.error(request, f"Shift {user_availability.shift_preferences} does not exist.")
            continue

        existing_hours_for_user = Schedule.objects.filter(
            user=user_availability.user_id,
            work_date=user_availability.day
        ).aggregate(models.Sum('shift_id__hours'))['shift_id__hours__sum'] or 0

        if existing_hours_for_user + shift.hours <= work_restrictions.max_daily_hours:
            min_hours_between_shifts = work_restrictions.min_hours_between

            if Schedule.objects.filter(
                    user=user_availability.user_id,
                    work_date__lt=user_availability.day,
                    work_date__gte=user_availability.day - timedelta(hours=min_hours_between_shifts)
            ).exists():
                continue

            schedule_entry = Schedule.objects.create(
                user=user_availability.user_id,
                shift_id=shift,
                work_date=user_availability.day
            )
            schedule_entries.append(schedule_entry)

    all_schedule_entries = Schedule.objects.all().order_by('work_date')

    return render(request, 'schedule/schedule_list.html', {'schedule_entries': all_schedule_entries})

@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def generate_pdf(request):
    # Pobierz posortowane wpisy według daty
    schedule_entries = Schedule.objects.order_by('work_date')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="schedule.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    data = [['User', 'Shift', 'Work Date']]

    for schedule_entry in schedule_entries:
        user = schedule_entry.user.username
        shift = schedule_entry.shift_id.shift_name


        work_date = make_aware(datetime.combine(schedule_entry.work_date, datetime.min.time()))

        # Użyj funkcji localtime
        work_date = timezone.localtime(work_date).strftime('%Y-%m-%d')
        data.append([user, shift, work_date])


    table = Table(data)


    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77aaff'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), styles['Heading1'].textColor),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), '#eeeeee'),
                        ('GRID', (0, 0), (-1, -1), 1, '#ffffff')])


    table.setStyle(style)

    content = [Paragraph("Schedule List", styles['Title']), table]

    doc.build(content)

    return response


