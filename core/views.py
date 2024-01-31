from django.shortcuts import render
import calendar
import datetime
from .models import Habit, Progress


def homepage(request):
    """
    Homepage view.

    Context variables:
        - `habits` - The user's Habit objects.
        - `progress` - The user's Progress objects for the current month.
        - `year` - The current year or the year given by the query parameter.
        - `month` - The current month or the month given by the query parameter.
        - `base_template`: The base template to extend from,
           depending on whether the request type is htmx or not.
    """

    # Get the current user, year, and month
    user = request.user
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    # If the year or month are not provided, use the current date
    if not year or not month:
        year = datetime.date.today().year
        month = datetime.date.today().month
    year = int(year)
    month = int(month)

    # Get the current user's habits and progress for the current month
    habits = Habit.objects.filter(user=user)
    progress = Progress.objects.filter(
        habit__user=user,
        date__year=year,
        date__month=month
    )

    # Determine the base template to use based on the request type
    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    context = {
        'habits': habits,
        'progress': progress,
        'year': year,
        'month': month,
        'base_template': base_template
    }
    return render(
        request,
        'core/index.html',
        context
    )
