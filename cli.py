from datetime import datetime
from model.event import Event
from model.recurring_event import *
from utility import get_event_list

if __name__ == '__main__':
    option = 'm'

    events = get_event_list(option)
    for event in events:
        event_id = event.get('id')
        summary = event.get('summary', 'No summary provided')
        start = event.get('start', {})
        end = event.get('end', {})
        start_time = start.get('dateTime', start.get('date'))
        end_time = end.get('dateTime', end.get('date'))
        recurring_event_id = event.get('recurringEventId')

        print(f"ID: {event_id}")
        print(f"Summary: {summary}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")
        if recurring_event_id:
            print(f"This is a recurring event. Recurring Event ID: {recurring_event_id}")
        else:
            print("This is a single event.")
        print()

    # title = "Test Event"
    # start_time = datetime(2024, 6, 9)
    # end_time = datetime(2024, 6, 9)
    # description = "This is a sample event description."
    # location = "Sample Location"
    # daylong = True
    # attendees = ["alice@example.com", "bob@example.com"]
    # sample_event = Event(title, start_time, end_time, description, location, daylong, attendees)
    # sample_event.add_event()

    # Create a recurrence rule
    # recurrence_rule = RecurrenceRule(
    #     freq="WEEKLY",
    #     interval=1,
    #     count=None,
    #     until=datetime(2024, 12, 31, 23, 59, 59),
    #     by_day=["MO", "WE", "FR"],
    #     by_month=[1, 6, 12],
    #     by_year_day=[1, 100, 200],
    #     by_hour=[9, 14]
    # )

    # Create a recurring event with the recurrence rule
    # recurring_event = RecurringEvent(
    #     title="Weekly Team Meeting",
    #     start_time=datetime(2024, 6, 6, 14, 0, 0),
    #     end_time=datetime(2024, 6, 6, 15, 0, 0),
    #     description="Weekly team meeting to discuss project progress.",
    #     location="Zoom",
    #     attendees=["alice@example.com", "bob@example.com"],
    #     recurrence=recurrence_rule
    # )
    #
    # recurring_event.add_event()




