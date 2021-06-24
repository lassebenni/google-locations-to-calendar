import os
import json
import boto3
from datetime import datetime

from gcalendar.calendar import Calendar
from gtimeline.timeline import Timeline
from weeronline.weather_to_gcal import WeatherToGoogleCalendar

bucket_name = os.environ.get('S3_BUCKET')
token_key = os.environ.get('TOKEN_KEY')
calendar_id = os.environ.get('CALENDAR_ID')
timeline_url = os.environ.get('TIMELINE_URL')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # fetch authorization token from S3
    auth_token = s3.get_object(
        Bucket=bucket_name, Key=token_key)['Body'].read()
    calendar = Calendar(calendar_id, auth_token)
    response_url = add_timeline_events(calendar, timeline_url)
    weather_results = WeatherToGoogleCalendar(calendar).create_weather_forecasts()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "timeline": f"Response URL: {response_url}",
            "weather": f"Weather forecast: {weather_results}",
        }),
    }

def add_timeline_events(calendar: Calendar, timeline_url: str = ""):
    timeline = Timeline(timeline_url)

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    url = timeline.create_timeline_url(date=date_str)

    event = calendar.create_calendar_event(summary='Timeline', description=f'Timeline for {today}', location=url, start_date=date_str, end_date=date_str)
    return calendar.insert_calender_event(event)


def test_local():
    file = open("token.pickle", 'rb')
    bytes = file.read()
    file.close()
    calendar_id = ''
    calendar = Calendar(calendar_id, bytes)
    # response_url = add_timeline_events(calendar, 'test')
    weather_calendar = WeatherToGoogleCalendar(calendar)
    # weather_calendar.delete_all_weather_events()
    weather_calendar.create_weather_forecasts()

if __name__ == "__main__":
    test_local()
