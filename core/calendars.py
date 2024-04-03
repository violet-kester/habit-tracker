import calendar
from datetime import date


class CustomHTMLCalendar(calendar.HTMLCalendar):
    """
    Custom HTMLCalendar that highlights today's date.
    """

    def __init__(self):
        super().__init__()
        self.today = date.today()

    def formatmonth(self, year, month, withyear=True):
        # When the formatmonth() method is called to generate an HTML calendar,
        # store the values for the year and month in the calendar instance,
        # so that they can be accessed by the formatday() method
        self.year, self.month = year, month
        # Then call the parent class's formatmonth() method as usual
        # to generate the HTML calendar
        return super().formatmonth(year, month, withyear)

    def formatday(self, day, weekday):
        # If the current day of the month being formatted is a "padding day",
        # meaning it falls outside of the month,
        # return an empty <td> for that day
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        # If the current day matches today's date,
        # add the class `.today` to its <td>
        elif day == self.today.day and (self.year, self.month) == (self.today.year, self.today.month):
            return f'<td class="{self.cssclasses[weekday]} today">{day}</td>'
        # Or else return the default <td>
        else:
            return f'<td class="{self.cssclasses[weekday]}">{day}</td>'


class HabitHTMLCalendar(calendar.HTMLCalendar):
    """
    Habit calendar

    A color-coded calendar that reflects the user's progress over time
    for a single habit.

    - Days of the month are togglers that can be clicked on to update
      the habit's completion status on that date.
    """
