from datetime import datetime
from typing import Optional, List
import typer
import logging
from config import SCOPES
from model.calendar import Calendar
from model.event import Event
from model.recurring_event import RecurrenceRule, RecurringEvent

app = typer.Typer()
logging.basicConfig(level=logging.INFO, format='%(message)s')
PERIODS = ['d', 'w', 'm']
FREQUENCIES = ["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]
DAYS_OF_WEEK = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
MONTHS = list(range(1, 13))
HOURS = list(range(0, 24))
DAYS_OF_YEAR = list(range(1, 367))


@app.command()
def list_events(period: str = typer.Argument(show_choices=True, metavar=",".join(PERIODS))):
    """
    List events from Google Calendar.

    This command retrieves and lists events from your Google Calendar within a specified time range.
    The time range can be specified using one of the following shorthand periods:

    - 'd' for today
    - 'w' for this week
    - 'm' for this month

    Args:
        period (str): A string representing the time period for which to list events.
                      Valid choices are 'd', 'w', 'm'.

    Example:
        To list events for today:
        $ python cli.py list-events d

        To list events for this week:
        $ python cli.py list-events w

        To list events for this month:
        $ python cli.py list-events m
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

    This command retrieves and displays the details of a calendar event
    based on the provided event ID. If the event is found, it logs the
    event details; if not, it logs a message indicating that the event
    was not found.

    Args:
        event_id (str): The unique identifier of the event to view.

    Example:
        To view an event with ID '12345', run the following command:

            python cli.py view-event 12345

    Notes:
        - Ensure that you have set up your Google Calendar API credentials
          and have a valid 'token.json' file or the necessary files for
          obtaining new credentials.
        - The event ID should be a valid identifier of an event in your
          Google Calendar.

    Logs:
        - If the event is found, logs the event details.
        - If the event is not found, logs "Event not found."
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
        Adds a new event to the Google Calendar.

        Args:
            title (str): The title of the event.
            start_time (datetime): The start date and time of the event.
                - To create a day-long event, provide only the date (without time).
                - To create an event with a specific time, provide both date and time.
            end_time (datetime): The end date and time of the event.
                - Should be after the start_time.
            description (Optional[str], optional): A description of the event. Default is None.
            location (Optional[str], optional): The location where the event will take place. Default is None.
            attendees (Optional[List[str]], optional): A list of email addresses of the attendees. Default is None.

        Example:
            python cli.py add-event "Team Meeting" "2024-06-10 10:00" "2024-06-10 11:00" \
           --description "Weekly team meeting to discuss project updates" \
           --location "Conference Room A" \
           --attendees "john.doe@example.com" "jane.smith@example.com"


        Notes:
            - Provide both date and time for start and end times to create an event with specific times.
            - Use date only for both start and end times to create a daylong event.
        """
    calendar = Calendar(SCOPES)
    event = Event(title=title, start_time=start_time, end_time=end_time, description=description,
                  location=location, attendees=attendees)
    if not event.is_valid():
        logging.error("Start and end times should either both have dates only, or both have dates and times.")
        return
    added_event = calendar.add_event(event)
    logging.info('Event created: %s' % (added_event.get('htmlLink')))


@app.command()
def quick_add_event(text: str):
    """
        Quickly adds an event to the Google Calendar using a simple text input.

        This function leverages the "Quick Add" feature of the Google Calendar API,
        which allows users to create an event using natural language input.
        For example, you can create an event by passing a string like "Dinner with Alice at 7pm tomorrow".

        Args:
            text (str): The natural language text describing the event details.

        Example:
            python cli.py quick-add-event("Team meeting at 10am tomorrow")

        The function initializes the Calendar object with the required scopes,
        then calls the quick_add method to create the event. If the event is created successfully,
        it prints the link to the created event in the Google Calendar.

        """
    calendar = Calendar(SCOPES)
    added_event = calendar.quick_add(text)
    logging.info('Event created: %s' % (added_event.get('htmlLink')))


@app.command()
def update_event(event_id: str, title: Optional[str] = None, start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None, description: Optional[str] = None,
                 location: Optional[str] = None, attendees: Optional[List[str]] = None):
    """
    Update an existing event by ID.

    Args:
        event_id (str): The unique identifier of the event to update.
        title (Optional[str]): The updated title of the event.
        start_time (Optional[datetime]): The updated start time of the event.
        end_time (Optional[datetime]): The updated end time of the event.
        description (Optional[str]): The updated description of the event.
        location (Optional[str]): The updated location of the event.
        attendees (Optional[List[str]]): The updated list of attendees for the event.

    Notes:
        - Provide the event ID along with at least one of the optional arguments to update the event.
        - The start time and end time should be provided either both with date only or both with date and time.
        - If the event ID is not valid or the event is not found, no update will be performed.
        - If any of the provided arguments are None, the corresponding attribute of the event will not be updated.

    Prints:
        If the event is successfully updated, prints the HTML link to the updated event.

    Example:
        To update the title of an event with ID '12345' to 'Team Meeting', run the following command:

            python cli.py update-event 12345 --title "Team Meeting"

        To update the start time and end time of the same event:

            python cli.py update-event 12345 --start_time "2024-06-10T10:00:00" --end_time "2024-06-10T11:00:00"
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

    if not event.is_valid():
        logging.error("Start and end times should either both have dates only, or both have dates and times.")
        return

    calendar = Calendar(SCOPES)
    updated_event = calendar.update_event(event)
    logging.info('Event created: %s' % (updated_event.get('htmlLink')))


@app.command()
def add_attendees(event_id: str, attendees: List[str]):
    """
        Add attendees to an existing event by ID.

        Args:
            event_id (str): The unique identifier of the event to which attendees will be added.
            attendees (List[str]): The list of email addresses of attendees to add to the event.

        Notes: - Provide the event ID along with the list of attendees to add them to the event. - If the event ID is
        not valid or the event is not found, no attendees will be added. - The provided email addresses in the
        attendees list will be added to the existing list of attendees. - If any of the provided email addresses are
        already attendees of the event, they will not be duplicated. - If the event ID is valid and attendees are
        successfully added, the HTML link to the updated event will be printed.

        Returns:
            None

        Example:
            To add attendees to an event with ID '12345', run the following command:

                python3 cli.py add-attendees 12345 john.doe@example.com jane.smith@example.com
        """
    calendar = Calendar(SCOPES)
    event = calendar.fetch_event_by_id(event_id)
    updated_event = calendar.add_attendees_to_event(event, attendees)
    print('Event created: %s' % (updated_event.get('htmlLink')))


@app.command()
def remove_attendees(event_id: str, attendees: List[str]):
    """
        Remove attendees from an existing event by ID.

        Args:
            event_id (str): The unique identifier of the event from which attendees will be removed.
            attendees (List[str]): The list of email addresses of attendees to remove from the event.

        Notes: - Provide the event ID along with the list of attendees to remove them from the event. - If the event
        ID is not valid or the event is not found, no attendees will be removed. - Only the provided email addresses
        in the attendees list will be removed from the existing list of attendees. - If any of the provided email
        addresses are not already attendees of the event, no action will be taken for them. - If the event ID is
        valid and attendees are successfully removed, the HTML link to the updated event will be printed.

        Returns:
            None

        Example:
            To remove attendees from an event with ID '12345', run the following command:

                python3 cli.py remove-attendees 12345 john.doe@example.com jane.smith@example.com
        """
    calendar = Calendar(SCOPES)
    event = calendar.fetch_event_by_id(event_id)
    updated_event = calendar.remove_attendees_from_event(event, attendees)
    print('Event created: %s' % (updated_event.get('htmlLink')))


@app.command()
def get_recurring_instances(event_id: str):
    """
        Retrieve instances of a recurring event by its ID.

        Args:
            event_id (str): The unique identifier of the recurring event to retrieve instances for.

        Notes:
            - Provide the event ID to fetch instances of a recurring event.
            - If the event ID is not valid or the event is not found, no instances will be retrieved.
            - This command returns all instances of the recurring event, including past and future occurrences.
            - The instances are printed to the console, displaying their titles.

        Returns:
            None

        Example:
            To retrieve instances of a recurring event with ID '12345', run the following command:

                python3 cli.py get-recurring-instances 12345
        """
    calendar = Calendar(SCOPES)
    recurring_instances = calendar.get_recurring_instances(event_id)
    for instance in recurring_instances:
        print(instance.title)


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
