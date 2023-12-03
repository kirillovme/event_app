from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from event.forms import EventForm
from event.models import Coordinate, Event, Weather
from django.contrib.auth.decorators import login_required
from infrastructure.gateways.api.weather_api_client import weather_async_client
from infrastructure.utils.async_login_decorator import async_login_required
from infrastructure.gateways.redis.redis_client import redis_client
from django.conf import settings


@login_required(login_url='/login')
@redis_client.invalidate_cache(key_format_list=[settings.EVENT_LIST_KEY_FORMAT])
def create_event(request: HttpRequest) -> HttpResponse:
    """Создает новое событие на основе данных из формы."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            coordinate, created = Coordinate.objects.get_or_create(latitude=latitude, longitude=longitude)
            event = form.save(commit=False)
            event.created_by = request.user
            event.coordinate = coordinate
            event.save()
            return redirect(reverse('create_weather', args=[coordinate.id]))
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})


@async_login_required
async def create_weather(request: HttpRequest, coordinate_id: int) -> HttpResponseRedirect:
    """Создает или обновляет данные о погоде для заданной координаты."""
    coordinate = await Coordinate.objects.aget(id=coordinate_id)
    weather_data = await weather_async_client.get_weather(coordinate.latitude, coordinate.longitude)
    weather = await Weather.objects.filter(coordinate=coordinate).afirst()
    if not weather:
        weather = Weather(coordinate=coordinate)
    weather.temperature = weather_data.temp
    weather.humidity = weather_data.humidity
    await weather.asave()
    return HttpResponseRedirect(reverse('get_events'))


@login_required(login_url='/login')
@redis_client.cache_result(key_format=settings.EVENT_LIST_KEY_FORMAT)
def get_events(request: HttpRequest) -> HttpResponse:
    """Получает список событий и связанных с ними данных о погоде."""
    events = Event.objects.all()
    event_weather_data = []
    for event in events:
        weather = Weather.objects.filter(coordinate=event.coordinate).first()
        event_weather_data.append({
            'event': event,
            'temperature': weather.temperature if weather else None,
            'humidity': weather.humidity if weather else None,
        })
    return render(request, 'event/get_events.html', {'event_weather_data': event_weather_data})


@login_required(login_url='/login')
@redis_client.invalidate_cache(key_format_list=[settings.EVENT_LIST_KEY_FORMAT])
def delete_event(request: HttpRequest, event_id: int) -> HttpResponseRedirect:
    """Удаляет событие."""
    event = Event.objects.filter(id=event_id).first()
    if event and event.created_by == request.user:
        event.delete()
    return HttpResponseRedirect(reverse('get_events'))


@login_required(login_url='/login')
@redis_client.invalidate_cache(key_format_list=[settings.EVENT_LIST_KEY_FORMAT])
def edit_event(request: HttpRequest, event_id: int) -> HttpResponse:
    """Редактирует существующее событие."""
    event = Event.objects.get(id=event_id)
    if request.user != event.created_by:
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            coordinate, created = Coordinate.objects.get_or_create(latitude=latitude, longitude=longitude)
            event = form.save(commit=False)
            event.created_by = request.user
            event.coordinate = coordinate
            event.save()
            return redirect(reverse('create_weather', args=[coordinate.id]))
    else:
        form = EventForm(instance=event,
                         initial={'latitude': event.coordinate.latitude, 'longitude': event.coordinate.longitude})
    return render(request, 'event/edit_event.html', {'form': form})
