from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from datetime import date, timezone
from .models import Habit, Progress
from .forms import HabitForm
from .calendars import CustomHTMLCalendar


def homepage(request):
    """
    Homepage view.

    From the homepage, users can click on links

    Context variables:
    - `habits` - The user's Habit objects.
    - `progress` - The user's Progress objects for the current day.
    - `html_calendar` - An instance of CustomHTMLCalendar.
    - `base_template` - The base template to extend from,
                        depending on whether the request type is htmx or not.
    """

    # Get the current user, year, and month from the request
    user = request.user
    year = request.GET.get('year', date.today().year)
    month = request.GET.get('month', date.today().month)

    # Check if the user is authenticated
    if user.is_authenticated:
        # Get user's habits and progress for the current day
        habits = Habit.objects.filter(user=user)
        progress = Progress.objects.filter(
            habit__user=user,
            date__year=year,
            date__month=month,
            date__day=date.today().day
        )
    # Otherwise, set habits and progress to empty values
    else:
        habits = []
        progress = []

    # Create an instance of CustomHTMLCalendar and format it
    html_calendar = CustomHTMLCalendar().formatmonth(year, month)

    # Determine which base template to extend from based on the request type
    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

    context = {
        'habits': habits,
        'progress': progress,
        'html_calendar': html_calendar,
        'base_template': base_template
    }
    return render(
        request,
        'core/index.html',
        context
    )


# Habit views -----------------------------------


@login_required
def habit(request, habit_slug):
    """
    Habit page view.

    Context:
    - `habit` - The Habit object. Contains habit meta data, stats, etc.
    - `habit_calendar` - A color-coded HTMLCalendar instance reflecting
                         the user's progress for this habit over time.
    - `base_template` - The base template to extend from,
                        depending on whether the request type is htmx or not.
    """

    # Determine which base template to extend from based on the request type
    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

    context = {
        'html_calendar': html_calendar,
        'base_template': base_template,
    }
    return render(request, 'core/habit.html', context)


@login_required
def add_habit(request):
    """
    Add habit view.

    - For POST requests, it creates a new habit in the database and
      returns HTML representing the new habit.
    - For other requests, it renders a form for adding a new habit.

    Context variables:
    - `form` - The HabitForm instance.
    - `base_template` - The base template to extend from,
                        depending on whether the request type is htmx or not.
    """

    # Authenticate and login user for POST requests
    if request.method == 'POST':
        form = HabitForm(data=request.POST)
        if form.is_valid():
            # Create a habit without saving it to the database
            habit = form.save(commit=False)
            # Assign habit to the user
            habit.user = request.user
            # Save the habit to the database
            habit.save()
            # Flash a success message
            messages.success(request, "Your new habit has been added.")
            # Redirect to the homepage
            return HttpResponse(status=204, headers={
                'HX-Redirect': reverse('core:homepage')
            })

    # Return a blank form for other requests
    else:
        form = HabitForm()

    # Determine which base template to extend from based on the request type
    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

    context = {
        'form': form,
        'base_template': base_template,
    }
    return render(request, 'core/forms/habit_form.html', context)


@login_required
def toggle_habit(request, habit_slug, date=None):
    """
    Toggle habit view.

    - Called by clicking a toggler for each habit on a single day.
    - Updates the habit's completion status in the database.
    - Renders a toggler with an updated background color
      based on completion status (white, gray, red, green, or gold).

    Context:
    - `habit` - The Habit object. Contains habit meta data, stats, etc.
    - `progress` - Contains data related to the habit's completion status on
                   the provided date, including the color used
                   to render the template background in the DOM.
    """

    habit = get_object_or_404(Habit, slug=habit_slug)
    date = date or timezone.now().date()

    # Retrieve the Progress object related to the habit and date
    try:
        progress = habit.Progress.get(date=date)
    # Or create a new Progress instance if it doesn't exist for this date
    except Progress.DoesNotExist:
        progress = Progress.objects.create(habit=habit, date=date)

    context = {
        'habit': habit,
        'progress': progress,
    }
    return render(request, 'core/habit_toggler.html', context)


# Auth routes -----------------------------------


def user_login(request):
    """
    Login view.

    - For POST requests, it authenticates and logs in the user,
      then redirects them to the homepage.
    - Otherwise, it renders the login page with an AuthenticationForm.

    Context variables:
    - `form` - An AuthenticationForm instance.
    """

    # For POST requests, authenticate, login, and redirect user to homepage
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to the homepage
            return HttpResponse(status=204, headers={
                'HX-Redirect': reverse('core:homepage')
            })

    # For other requests, render a blank AuthenticationForm
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'core/forms/login_form.html', context)


def user_logout(request):
    """
    Logout view.

    - Logs the user out and redirects them to the homepage.
    """

    logout(request)

    return HttpResponse(
        status=204,
        headers={'HX-Redirect': reverse('core:homepage')}
    )


def user_register(request):
    """
    Register view.
    """

    pass
