from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
import calendar
import datetime
from datetime import date
from .models import Habit, Progress
from .forms import HabitForm


def homepage(request):
    """
    Homepage view.

    Context variables:
    - `habits` - The user's Habit objects.
    - `progress` - The user's Progress objects for the current day.
    - `html_cal` - An instance of HTMLCalendar for rendering the calendar.
    - `base_template` - The base template to extend from,
                        depending on whether the request type is htmx or not.
    """

    # Get the current user, year, and month from the request
    user = request.user
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)

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

    # Write a custom formatday method for adding custom styling to the calendar
    def formatday(day, weekday):
        # If the day is zero, return an empty cell
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        # Create a date object for the day
        date = datetime.date(year, month, day)
        # Check if the date is today
        is_today = date == datetime.date.today()
        # Create a CSS class for the date cell based on the conditions
        if is_today:
            css_class = "cal-today"
        else:
            css_class = "cal-not-today"
        # Return the HTML code for the date cell with the habit names
        return f'<td class="{css_class}">{day}</td>'

    # Create an HTMLCalendar instance
    cal = calendar.HTMLCalendar()
    # Override the default formatday method on the HTMLCalendar instance
    cal.formatday = formatday
    # Format the entire month as an HTML table
    html_cal = cal.formatmonth(year, month)

    # Determine which base template to extend from based on the request type
    if request.htmx:
        base_template = '_partial.html'
    else:
        base_template = '_base.html'

    context = {
        'habits': habits,
        'progress': progress,
        'html_cal': html_cal,
        'base_template': base_template
    }
    return render(
        request,
        'core/index.html',
        context
    )


# Habit routes ----------------------------------


@login_required
def add_habit(request):
    """
    Add habit view.

    - For POST requests, it creates a new habit in the database and
      returns HTML representing the new habit.
    - For other requests, it renders a form for adding a new habit.

    Context variables:
    - `form` - The AuthenticationForm instance.
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
            habit.user = form.get_user()
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
    return render(request, 'core/habit_toggler.html', context)


@login_required
def toggle_habit(request, habit_slug):
    """
    Toggle habit view.

    - Called by clicking a toggler for each habit on a single day.
    - Updates the habit's completion status in the database.
    - Renders a red, green, or gray toggler based on completion status.
    """

    context = {
        'habit': habit,
        'current_color': current_color,
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
