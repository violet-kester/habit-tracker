import calendar
from datetime import date


class CustomHTMLCalendar(calendar.HTMLCalendar):
    """
    Custom calendar

    A custom HTML calendar class subclassed by all other custom HTML calendars.

    - Highlights today's date.
    """

    def __init__(self):
        super().__init__()
        self.today = date.today()

    def formatmonth(self, year, month, withyear=True):
        """
        When the `formatmonth()` method is called to generate an HTML calendar,
        store the values for the year and month in the calendar instance,
        so that they're accesseible to the other formatting methods below.

        Then call the parent class's `formatmonth()` method to generate
        the HTML table calendar as usual.
        """
        self.year, self.month = year, month
        return super().formatmonth(year, month, withyear)

    def formatmonthname(self, year, month, withyear=True):
        """
        Overrides the parent class's `formatmonthname()` method in order to
        add a custom class name `.month-header` to the month header row
        for styling purposes.
        """

        if withyear:
            return f'<tr><th colspan="7" class="month-header">{calendar.month_name[month]} {year}</th></tr>'
        else:
            return f'<tr><th colspan="7" class="month-header">{calendar.month_name[month]}</th></tr>'

    def formatday(self, day, weekday):
        """
        Overrides the parent class's `formatday()` method in order to
        add a custom class `.today` to today's date cell for styling purposes.
        """

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


class HabitHTMLCalendar(CustomHTMLCalendar):
    """
    Habit calendar

    A custom HTML calendar class that reflects the user's progress over time
    for a single habit.

    - Days of the month contain color-coded togglers that can be clicked on
      to update the habit's completion status for that date.
    """

    def formatday(self, day, weekday):
        """
        Overrides the parent class's `formatday()` method in order to
        include togglers for updating completion status
        inside each day's table cell.
        """

        # Call the `formatday()` method of the superclass `CustomHTMLCalendar`
        # to maintain the highlighting of today's date
        day_cell = super().formatday(day, weekday)

        # TODO:
        # Implement logic for determining completion status
        # Modify day_cell to include bg color attribute based on completion
        # Add HTML for toggler inside <td>

        return day_cell
