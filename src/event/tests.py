from collections import namedtuple
from datetime import date
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import AsyncClient, Client, TestCase
from django.urls import reverse

from event.models import Coordinate, Event, Weather

MockWeatherData = namedtuple('MockWeatherData', ['temp', 'humidity'])


class EventViewTests(TestCase):
    mock_weather_data = MockWeatherData(temp=25, humidity=60)

    def setUp(self):
        """Настройка тестового клиента, асинхронного клиента и пользователя перед выполнением тестов."""
        self.client = Client()
        self.async_client = AsyncClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.async_client.login(username='testuser', password='12345')
        self.coordinate = Coordinate.objects.create(latitude=10, longitude=20)
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Event Description',
            coordinate=self.coordinate,
            start_date=date.today(),
            end_date=date.today(),
            created_by=self.user
        )

    def test_create_event_post_valid(self):
        """Тест на успешное создание события с валидными данными."""
        url = reverse('create_event')
        data = {'latitude': 30, 'longitude': 40, 'title': 'New Event', 'description': 'New Description',
                'start_date': date.today(), 'end_date': date.today()}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_create_event_post_invalid(self):
        """Тест на обработку невалидных данных при создании события."""
        url = reverse('create_event')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

    def test_create_event_get(self):
        """Тест на получение страницы создания события."""
        url = reverse('create_event')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch('infrastructure.gateways.api.weather_api_client.weather_async_client.get_weather',
           return_value=mock_weather_data)
    async def test_create_weather(self, mock_get_weather):
        """Асинхронный тест на создание данных о погоде для координат."""
        url = reverse('create_weather', args=[self.coordinate.id])
        response = await self.async_client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(await Weather.objects.filter(coordinate=self.coordinate).aexists())

    def test_get_events(self):
        """Тест на получение страницы со списком событий."""
        url = reverse('get_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_event_get_authorized(self):
        """Тест на проверку доступа к редактированию события авторизованным пользователем."""
        url = reverse('edit_event', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_event_get_unauthorized(self):
        """Тест на перенаправление при попытке редактирования события неавторизованным пользователем."""
        User.objects.create_user(username='anotheruser', password='12345')
        self.client.login(username='anotheruser', password='12345')
        url = reverse('edit_event', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_event_post_valid(self):
        """Тест на обновление события с валидными данными."""
        url = reverse('edit_event', args=[self.event.id])
        data = {'latitude': 50, 'longitude': 60, 'title': 'Updated Event', 'description': 'Updated Description',
                'start_date': date.today(), 'end_date': date.today()}
        self.client.post(url, data)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event')

    def test_delete_event(self):
        """Тест на успешное удаление события."""
        new_event = Event.objects.create(
            title='Event to Delete',
            description='Description of event to delete',
            coordinate=self.coordinate,
            start_date=date.today(),
            end_date=date.today(),
            created_by=self.user
        )
        self.assertTrue(Event.objects.filter(id=new_event.id).exists())
        url = reverse('delete_event', args=[new_event.id])
        response = self.client.get(url)
        self.assertFalse(Event.objects.filter(id=new_event.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_events'))
