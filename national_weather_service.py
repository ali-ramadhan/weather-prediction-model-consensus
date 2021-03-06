import json
import requests
import logging.config
from dateutil.parser import parse

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def nws_temp_time_series(lat, lon):
    api_url = "https://api.weather.gov/points/" + str(lat) + "," + str(lon)
    response = requests.get(api_url)

    if response.status_code != 200:
        response.raise_for_status()

    point = json.loads(response.content)

    wfo = point['properties']['cwa']
    X = point['properties']['gridX']
    Y = point['properties']['gridY']
    forecast_url = point['properties']['forecast']
    hourly_forecast_url = point['properties']['forecastHourly']

    logger.info("National Weather Service: WFO={:s}, (X,Y)=({:d},{:d})".format(wfo, X, Y))
    logger.info("Forecast URL: {:s}".format(forecast_url))
    logger.info("Hourly forecast URL: {:s}".format(hourly_forecast_url))

    response = requests.get(hourly_forecast_url)
    hourly_forecast = json.loads(response.content)

    times = []
    temps = []

    for i, fe in enumerate(hourly_forecast['properties']['periods']):
        time = fe['startTime']
        T = fe['temperature']
        wind_speed = fe['windSpeed']
        wind_dir = fe['windDirection']
        description = fe['shortForecast']

        times.append(parse(time))
        temps.append(T)

    return times, temps

