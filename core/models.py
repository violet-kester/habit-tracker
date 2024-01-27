from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Habit(models.Model):
    """A model class that represents a habit to track."""

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='habits')

    def get_absolute_url(self):
        """
        Returns the absolute URL of the post detail view.

        For example:
            habit = Habit.objects.get(slug='wake-up-early')
            habit.get_absolute_url()

        Returns:
            'https://example.com/user/habits/wake-up-early/'
        """

        return reverse('blog:post_detail',
                       args=[self.slug])
