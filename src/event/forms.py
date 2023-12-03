from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    """Форма для создания события."""

    latitude = forms.FloatField()
    longitude = forms.FloatField()

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date']
