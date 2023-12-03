from typing import Any

import requests
from celery import shared_task
from django.conf import settings

from event.models import Event, Weather


@shared_task
def update_weather_for_events() -> None:
    """Периодическая задача на обновление прогноза погода по координатам."""
    for event in Event.objects.all():
        weather_data = get_weather_for_coordinate(event.coordinate.latitude, event.coordinate.longitude)
        update_or_create_weather(event.coordinate, weather_data)


def get_weather_for_coordinate(lat: float, lon: float) -> dict[str, Any]:
    """Получает данные о погоде по заданным координатам широты и долготы."""
    params = {
        'lat': lat,
        'lon': lon,
        settings.WEATHER_API_KEY: settings.WEATHER_API_TOKEN
    }
    response = requests.get(settings.WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to fetch weather data: {response.status_code}')


def update_or_create_weather(coordinate, weather_data: dict[str, Any]) -> None:
    """Обновляет или создает запись о погоде в базе данных."""
    Weather.objects.update_or_create(
        coordinate=coordinate,
        defaults={
            'temperature': weather_data['temp'],
            'humidity': weather_data['humidity'],
        }
    )
