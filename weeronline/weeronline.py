import json
from typing import List
import requests

from datetime import datetime, timedelta
from dataclasses import dataclass

BROWSER_URL = "https://www.weeronline.nl/Europa/Nederland/Utrecht/4058499"
URL = "https://www.weeronline.nl/api/mosForecastService;geoAreaId=4058499;interval=1D;offsetEnd=13;offsetStart=0?returnMeta=true" # Utrecht, Netherlands

PAYLOAD={}
HEADERS = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
		'Accept': '*/*',
		'Accept-Language': 'nl,en-US;q=0.7,en;q=0.3',
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		'Referer': 'https://www.weeronline.nl/Europa/Nederland/Utrecht/4058499',
		'Cookie': 'gdpr-auditId=7b45fb94-2bd6-4cb6-847e-3b547739f968; gdpr-last-interaction=1618210941.128; gdpr-config-version=53; euconsent-v2=CPA1BfNPEh2TkADABBNLBVCsAP_AAH_AAAAAGrNf_X_fb2tj-_599_t0eY1f9_63v-wzjheNs-8Nyd_X_L8Xv2MyvB36pq4KuR4ku3bBAQNtHOnUTQmR4IlVqTLsak2Mr7NKJ7LEmlsbe2dYGHtPn9VT-ZKZr07v___7_3______75__b__90DUwCTDUvgIExLHAkmjSqFECEK4kKgFABRQjC0TWEBK4KdlcBHqCBAAhNQEYEQIMQUYsAgAEAgCSiIAQA8EAiAIgEAAIAVICEABEgCCwAsDAIABQDQsAIoAhAkIMjgqOUwICJFooJ5IwBILvYwAA.f_gAAAAAAAA; cconsent-v2=CPA1BfNPEh2TkADABBNLBVCgAPgAAAAAAAABmlQHQACQAHAAgAIYAoYBpAGmANoAcABFgCPwFSAVMArIBYgCyCdpE74J7cUJoo0BU5itXFeCLcQW-ovkRfajBVGI2MvMZpQAAAAA.YAAAAAAAAAA; addtl_consent=1~89.108.167.317.448.867.1095.1201.1716.1765.2177.2213.2373.2571.3043.3130; __cfduid=db50ec340b44e873008b93b5c5de0d8a41618210935; proxy_session=s%3AsZF-TpZ8nCgvdP9T4gYnL6iyf_V1hjrx6NSqGPcu.TJ8un%2BNQxM61Ewp%2FHQ%2ByqHphcdzbSHGYfB%2Bwpz2i4L8; geo-location={"country":"NL","region":"UT"}; gdpr-dau=true; gdpr-dau-log-sent=true',
		'If-None-Match': 'W/"a36c-Fp5VxsV47XPkR7O/j5ryy9dsJIE"',
		'TE': 'Trailers'
}


@dataclass
class WeatherForecast:
  date: str
  digit: int
  temperature: float
  url: str

class Weeronline(object):
  date: datetime


  """Weeronline.nl data fetcher."""
  def __init__(self, date: datetime):
    self.date = date

  def fetch_forecasts(self) -> List[WeatherForecast]:
    result = []

    response = requests.request("GET", URL, headers=HEADERS, data=PAYLOAD)
    resp_json = json.loads(response.text)
    if resp_json:
      data = resp_json['data']

    if data:
      weather_digits = [d['digits']['weather'] for d in data]
      weather_temps = [round(d['temperature']['feelsLike'],1) for d in data]

      delta = 0
      for i, v in enumerate(data):
        day = self.date + timedelta(days=delta)
        weather_result = WeatherForecast(
          date=day.strftime("%Y-%m-%d"),
          digit=weather_digits[i],
          temperature= weather_temps[i],
          url=BROWSER_URL
        )

        result.append(weather_result)
        delta+=1

    return result
