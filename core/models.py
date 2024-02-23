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

    - Has a one-to-many relationship with the Progress model.
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='habits')
    slug = models.SlugField(max_length=250,
                            unique=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)

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

    - Stores the completion status as a boolean value.
    - Has a many-to-one relationship with the Habit model.
    """

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.habit.name} - {self.date}'
