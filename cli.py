from datetime import datetime, date
from typing import Optional, List

import typer
import logging
from config import SCOPES
from model.calendar import Calendar
from model.event import Event
from model.recurring_event import RecurrenceRule, RecurringEvent

app = typer.Typer()
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
FREQUENCIES = ["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]
DAYS_OF_WEEK = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
MONTHS = list(range(1, 13))
HOURS = list(range(0, 24))
DAYS_OF_YEAR = list(range(1, 367))


@app.command()
def list_events(period: str):
    """
    List events from Google Calendar.
    Use 'd' for today, 'w' for this week, 'm' for this month.
    """
    logging.info('Getting events within the specified time range...\n')
    calendar = Calendar(SCOPES)
    events = calendar.get_event_list(period)
    if not events:
        logging.info("No events found.")
    for event in events:
        logging.info(event)


@app.command()
def view_event(event_id: str):
    """
    View event details by ID.
    """
    calendar = Calendar(SCOPES)
    event = calendar.fetch_event_by_id(event_id)
    if event:
        logging.info(event)
    else:
        logging.info("Event not found.")


@app.command()
def add_event(title: str, start_time: datetime, end_time: datetime, description: Optional[str] = None,
              location: Optional[str] = None, attendees: Optional[List[str]] = None):
    """
    Add a new event.

    Hints:
    - To create a daylong event, provide only the date without time.
    - To create an event with specific time, provide both date and time.
    """

    if isinstance(start_time, date) and isinstance(end_time, date):
        daylong = True

    elif isinstance(start_time, datetime) and isinstance(end_time, datetime):
        daylong = False
    else:
        logging.info("Start and end times should either both have date only or both have date and time.")
        return

    calendar = Calendar(SCOPES)
    event = Event(title=title, start_time=start_time, end_time=end_time, description=description,
                  location=location, daylong=daylong, attendees=attendees)
    added_event = calendar.add_event(event)
    print('Event created: %s' % (added_event.get('htmlLink')))


@app.command()
def update_event(event_id: str, title: Optional[str] = None, start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None, description: Optional[str] = None,
                 location: Optional[str] = None, attendees: Optional[List[str]] = None):
    """
    Update an existing event by id.

    Hints:
    - To update a daylong event, provide only the date without time.
    - To update an event with specific time, provide both date and time.
    """

    calendar = Calendar(SCOPES)
    event = calendar.fetch_event_by_id(event_id)
    if title:
        event.title = title
    if start_time:
        event.start_time = start_time
    if end_time:
        event.end_time = end_time
    if description:
        event.description = description
    if location:
        event.location = location
    if attendees:
        event.attendees = attendees

    if isinstance(event.start_time, date) and isinstance(event.end_time, date):
        event.daylong = True
    elif isinstance(start_time, datetime) and isinstance(end_time, datetime):
        event.daylong = False
    else:
        logging.info("Start and end times should either both have date only or both have date and time.")
        return

    calendar = Calendar(SCOPES)
    updated_event = calendar.update_event(event)
    print('Event created: %s' % (updated_event.get('htmlLink')))


@app.command()
def add_attendees(event_id: str, attendees: List[str]):
    calendar = Calendar(SCOPES)
    event = calendar.fetch_event_by_id(event_id)
    updated_event = calendar.add_attendees_to_event(event, attendees)
    print('Event created: %s' % (updated_event.get('htmlLink')))



@app.command(help="Add a new recurring event.")
def add_recurring_event(
        title: str = typer.Argument(..., help="Title of the event."),
        start_time: datetime = typer.Argument(..., help="Start time of the event. (YYYY-MM-DDTHH:MM)"),
        end_time: datetime = typer.Argument(..., help="End time of the event. (YYYY-MM-DDTHH:MM)"),
        freq: str = typer.Option(..., "--freq", help="Frequency of the recurrence.", show_choices=True,
                                 metavar=",".join(FREQUENCIES)),
        interval: int = typer.Option(1, "--interval", help="Interval of the recurrence."),
        count: Optional[int] = typer.Option(None, "--count", help="Number of occurrences."),
        until: Optional[datetime] = typer.Option(None, "--until",
                                                 help="End date of the recurrence. (YYYY-MM-DDTHH:MM)"),
        by_day: Optional[List[str]] = typer.Option(None, "--by-day", help="Days of the week to recur (e.g., MO, TU).",
                                                   show_choices=True, metavar=",".join(DAYS_OF_WEEK)),
        by_month: Optional[List[int]] = typer.Option(None, "--by-month", help="Months to recur.", show_choices=True,
                                                     metavar="1-12"),
        by_year_day: Optional[List[int]] = typer.Option(None, "--by-year-day", help="Days of the year to recur.",
                                                        show_choices=True, metavar="1-366"),
        by_hour: Optional[List[int]] = typer.Option(None, "--by-hour", help="Hours of the day to recur.",
                                                    show_choices=True, metavar="0-23"),
        description: Optional[str] = typer.Option(None, "--description", "-d", help="Description of the event."),
        location: Optional[str] = typer.Option(None, "--location", "-l", help="Location of the event."),
        attendees: Optional[List[str]] = typer.Option(None, "--attendees", "-a", help="List of attendees.")
):
    """
    Add a new recurring event.

    Hints:
    - To create a daylong event, provide only the date without time.
    - To create an event with specific time, provide both date and time.
    """
    daylong = False
    if start_time.time() == datetime.min.time() and end_time.time() == datetime.max.time():
        daylong = True

    recurrence = RecurrenceRule(
        freq=freq,
        interval=interval,
        count=count,
        until=until,
        by_day=by_day,
        by_month=by_month,
        by_year_day=by_year_day,
        by_hour=by_hour
    )
    recurring_event = RecurringEvent(
        title=title,
        start_time=start_time,
        end_time=end_time,
        recurrence=recurrence,
        description=description,
        location=location,
        daylong=daylong,
        attendees=attendees
    )
    calendar = Calendar(SCOPES)
    added_event = calendar.add_event(recurring_event)
    print(added_event)
    print('Event created: %s' % (added_event.get('htmlLink')))


if __name__ == '__main__':
    app()
