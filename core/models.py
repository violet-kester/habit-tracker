from datetime import timedelta, timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    """
    A model class that extends Django's User model.
    Stores additional data about the user.

    - Has a one-to-one relationship with the User model.
    - Has a one-to-many relationship with the Habit model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    habits = models.ManyToManyField('Habit', related_name='habits')


class Habit(models.Model):
    """
    A model class that represents a habit being tracked.

    - Has a many-to-one relationship with the User model.
    - Has a one-to-many relationship with the Progress model.
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='habits')
    slug = models.SlugField(max_length=250,
                            unique=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    # Target number of times/week. 7 = everyday, 1 = once a week.
    weekly_rate = models.IntegerField(blank=True, default=7)
    # Tracking can be paused for individual habits
    paused = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method in order to
        initialize a Progress object when a new Habit is created.
        """

        # Determine if the save method is being called on
        # a new instance of Habit that hasn’t been saved before
        is_new = self._state.adding

        # Then save the habit instance
        super().save(*args, **kwargs)

        # If the habit is a new one, initialize an instance of Progress for it
        if is_new:
            Progress.objects.create(habit=self, date=timezone.now().date())

    def get_absolute_url(self):
        """
        Returns the absolute URL of a habit's detail view.

        For example:
            habit = Habit.objects.get(slug='wake-up-early')
            habit.get_absolute_url()

        Returns:
            'https://example.com/user/habits/wake-up-early/'
        """

        return reverse('blog:post_detail', args=[self.slug])

    def __str__(self):
        return f'Habit: {self.name}'


class Progress(models.Model):
    """
    A model class that represents the completion status of a habit on a date.

    - Stores a habit's completion status on a given date as a boolean value.
    - Stores a corresponding color value used to visually represent
      completion status in the DOM (e.g. in calendars, togglers).
    - Has a many-to-one relationship with the Habit model, one instance for
      each day.
    """

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def get_completion_status(self):
        """
        Returns a string completion status for the habit on this day.

        Returns:
        - 'completed_for_day' - Completed for the day.
        - 'completed_for_week' - Completed for the week (weekly rate met).
        - 'incomplete' - Not yet complete.
        - 'missed' - Incomplete + in the past.
        - 'paused' - Habit tracking paused on this day.
        """

        # Check if the habit is paused or inactive
        if self.paused:
            return 'paused'

        # Calculate the start and end of the week based on the date
        start_of_week = self.date - timedelta(days=self.date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Count the number of completed Progress objects for this week
        completed_this_week = Progress.objects.filter(
            habit=self.habit,
            date__range=(start_of_week, end_of_week),
            completed=True
        ).count()

        # Compute the completion status and return it
        if completed_this_week >= self.habit.weekly_rate:
            return 'completed_for_week'
        elif self.completed:
            return 'completed_for_day'
        elif self.date < timezone.now():
            return 'missed'
        else:
            return 'incomplete'

    @property
    def color(self):
        """
        A property that dynamically returns a color value based on
        the completion status for this date.
        """

        # Mapping of completion statuses to their corresponding color codes
        status_color_map = {
            'completed_for_week': 'gold',
            'completed_for_day': 'green',
            'missed': 'red',
            'incomplete': 'white',
            'paused': 'gray'
        }

        # Retrieve the color using the completion status or default to gray
        return status_color_map.get(self.get_completion_status(), 'gray')

    def __str__(self):
        return f'Progress: {self.habit.name} - {self.date}'
