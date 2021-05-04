from datetime import datetime
from gcalendar.calendar import Calendar, CalendarEvent
from weeronline.weeronline import Weeronline, WeatherForecast
from dataclasses import dataclass
from typing import List

@dataclass
class WeatherEvent:
  calendar_event: CalendarEvent = None
  forecast: WeatherForecast = None
  summary: str = ""
  location: str = ""
  date: str = ""

  def __post_init__(self):
    if self.calendar_event:
      self.summary = self.calendar_event.summary
      self.location = self.calendar_event.location
      self.summary = self.calendar_event.summary
      self.date = self.calendar_event.start_date
    if self.forecast:
      self.summary = f'Weeronline: {self.forecast.digit} - {self.forecast.temperature}°C'
      self.location = self.forecast.url
      self.date = self.forecast.date


class WeatherToGoogleCalendar(object):
  """docstring for WeatherToGoogleCalendar ."""

  calendar: Calendar
  weeronline: Weeronline

  date : datetime
  date_str: str = ""

  def __init__(self,calendar: Calendar, date: datetime = None):
    self.calendar = calendar

    if not date:
      date = datetime.now()

    self.date = date
    self.date_str = self.date.strftime("%Y-%m-%d")
    self.weeronline = Weeronline(date=date)

  def create_weather_forecasts(self):
    result = []

    forecasts = self.weeronline.fetch_forecasts()

    existing_events = self.list_weather_events(self.date_str)
    date_event_map = {e.date: e for e in existing_events}

    for forecast in forecasts:
      existing_forecast = date_event_map.get(forecast.date, None)

      # update existing forecast
      if existing_forecast:
        updated_forecast = WeatherEvent(forecast=forecast,calendar_event=existing_forecast.calendar_event)

        if existing_forecast.calendar_event.summary != updated_forecast.summary:
          updated_forecast.calendar_event.body['summary'] = updated_forecast.summary
          result.append(self.update_weather_event(updated_forecast))

      # otherwise add new forecasts
      else:
        weather_event = WeatherEvent(forecast=forecast)
        result.append(self.add_weather_event(weather_event))

    return result

  def list_weather_events(self, start_date: str = "") -> List[WeatherEvent]:
    result: List[WeatherEvent] = []

    if not start_date:
      tz_iso_stamp = self.date.astimezone().isoformat()
    else:
      tz_iso_stamp = datetime.strptime(start_date, '%Y-%m-%d').astimezone().isoformat()

    events = self.calendar.list_events(query='Weeronline', min_datetime = tz_iso_stamp)

    for event in events:
      result.append(WeatherEvent(calendar_event=event))

    return result

  def update_weather_event(self, event: WeatherEvent):
      return self.calendar.update_event(calendar_event=event.calendar_event)

  def add_weather_event(self, event: WeatherEvent):
      calendar_event =  self.calendar.create_calendar_event(summary=event.summary, location=event.location, start_date=event.date, end_date=event.date)
      return self.calendar.insert_calender_event(calendar_event=calendar_event)

  def delete_all_weather_events(self):
    weather_events = self.list_weather_events()
    for event in weather_events:
      self.calendar.delete_event(calendar_event=event.calendar_event)
