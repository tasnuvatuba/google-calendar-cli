# Google Calendar CLI

This project provides a command-line interface (CLI) to interact with Google Calendar system. You can list, view, add, update, and delete events, including managing recurring events and attendees.

## Features

- **List Events**: List all events of today, this week or this month (use argument 'd' for today, 'w' for this week, 'm' for this month)
- **View Event**: View the details of an event by its ID.
- **Add Event**:  Add a new event with specified title, start time, end time, description, location, and attendees.
- **Quick Add Event**: Quickly add an event using natural language input.
- **Update Event**: Update an existing event by its ID with optional new details such as title, start time, end time, description, location, and attendees.
- **Add Attendees**: Add attendees to an existing event by its ID.
- **Remove Attendees**: Remove attendees from an existing event by its ID.
- **Get Recurring Instances**:  List all instances of a recurring event by its ID.
- **Add Recurring Event**: Add a new recurring event with specified recurrence rules, title, start time, end time, description, location, and attendees.
- **Delete Event**: Delete an event by its ID.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/tasnuvatuba/google-calendar-cli
    cd google-calendar-cli
    ```

2. Set up a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```
   
4. **Set up Google Calendar API**:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
    - Enable the Google Calendar API.
    - Create OAuth 2.0 credentials (OAuth client ID).
    - Download the `credentials.json` file and place it in the root directory of this project.

## Usage
### List Events
```bash
python3 cli.py list-events w

```

### View Event
```bash
python3 cli.py add-event python3 cli.py view-event 123445

```

### Add Event
```bash
python3 cli.py add-event "Team Meeting" "2024-06-10 10:00" "2024-06-10 11:00" \
           --description "Weekly team meeting to discuss project updates" \
           --location "Conference Room A" \
           --attendees "john.doe@example.com" "jane.smith@example.com"
```

### Quick Add Event
```bash
python3 cli.py quick-add-event "Team meeting at 10am tomorrow"
```

### Update Event
```bash
python3 cli.py update-event 12345 --title "Team Meeting"
```

### Add Attendees
```bash
python3 cli.py add-attendees 12345 john.doe@example.com jane.smith@example.com
```

### Remove Attendees
```bash
python3 cli.py remove-attendees 12345 john.doe@example.com jane.smith@example.com
```

### Get Recurring Instances
```bash
python3 cli.py get-recurring-instances 12345
```

### Add Recurring Event
```bash
python3 cli.py add-recurring-event "Team Meeting" "2024-06-10T09:00:00" "2024-06-10T10:00:00" weekly
                
```

### Delete Event
```bash
python3 cli.py delete-event 12345
```


## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss your ideas.