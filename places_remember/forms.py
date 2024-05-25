from django import forms
from .models import Memory


class MemoryForm(forms.ModelForm):
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Memory
        fields = ['title', 'comment', 'latitude', 'longitude']
