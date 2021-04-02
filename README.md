# Google Locations to Google Calendar Event

Create a daily Event in Google Calendar to quickly link the Locations overview from Google Maps to
the specific day.

## Code

Based on example code in <https://developers.google.com/calendar/quickstart/python>.

## Steps

1. Create API Key for use, see link.
2. Connect to Google Calendar API, use `calendar.events` SCOPE for permissions.

- If this is the first time, you have to authorize the app using the browser login flow.
- After the first time, the credentials are pickled and kept in `token.pickle`, which can be re-used for future API calls.

3. Create a new Event, inserting the link [Locations](https://www.google.se/maps/timeline?hl=nl&authuser=0&pb=!1m2!1m1!1s2020-08-20) into the event with the current date.

## TODO

- Find out how long the token is valid.
