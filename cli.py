import typer

from model.event import Event
from utility import get_event_list

app = typer.Typer()


@app.command()
def list_events(period: str):
    """
    List events from Google Calendar.
    Use 'd' for today, 'w' for this week, 'm' for this month.
    """
    json_events = get_event_list(period)
    events = []
    for json_event in json_events:
        events.append(Event.from_json(json_event))
    for event in events:
        print(event)


@app.command()
def add_event():
    print("Not implemented yet")


if __name__ == '__main__':
    app()
