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
    A model class that represents a habit to track.

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
    # Number of times/week. 7 = everyday, 1 = once a week.
    weekly_rate = models.IntegerField(blank=True, default=7)

    def get_absolute_url(self):
        """
        Returns the absolute URL of a habit's detail view.

        For example:
            habit = Habit.objects.get(slug='wake-up-early')
            habit.get_absolute_url()

        Returns:
            'https://example.com/user/habits/wake-up-early/'
        """

        return reverse('blog:post_detail',
                       args=[self.slug])

    def __str__(self):
        return self.name


class Progress(models.Model):
    """
    A model class that represents the completion status of a habit on a date.

    - Stores a habit's completion status on a given date as a boolean value.
    - Stores a color value for each date used to visually represent
      completion status in the DOM (e.g. in the calendar).
    - Has a many-to-one relationship with the Habit model.
    """

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    # TODO: Implement logic for color selection
    color = models.CharField(default='gray')
    # Is the number of Progress.completed for this habit for this week > weekly_rate?
    # If so, set color to gold
    # Is Progress.completed True for today?
    # If so, set color to green
    # Is the specified date in the past and Progress.complete False?
    # If so, set the color to red

    def __str__(self):
        return f'{self.habit.name} - {self.date}'
