from django import forms
from django.contrib.auth import get_user_model
import datetime

now = datetime.datetime.now().replace(tzinfo=None)

class TripForm(forms.Form):
    name = forms.CharField(label="Trip Name", widget=forms.TextInput(
        attrs={"class": "form-control", 'id': 'form_name', "placeholder": "Give your trip a name", }))
    location = forms.CharField(label="Destination", widget=forms.TextInput(
        attrs={"class": "form-control", 'id': 'form_location', "placeholder": "Where are you traveling to?", }))
    description = forms.CharField(label="Description", widget=forms.Textarea(
        attrs={'class': 'form-control', 'id': 'form_description', 'rows': '3'}))
    start_date = forms.DateTimeField(label='Start Date', widget=forms.DateTimeInput(
        attrs={'type': 'date', 'class': 'form-control', 'id': 'form_start_date'}))
    end_date = forms.DateTimeField(label="End Date", widget=forms.DateInput(
        attrs={'type': 'date', "class": "form-control", 'id': 'form_end_date'}))
    rating = forms.IntegerField(label="Rating", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'id': 'form_rating', 'min': '0', 'max': '5'}))  # Add the rating field

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        location = cleaned_data.get('location')
        description = cleaned_data.get('description')
        start_date = cleaned_data.get('start_date').replace(tzinfo=None)
        end_date = cleaned_data.get('end_date').replace(tzinfo=None)
        rating = cleaned_data.get('rating')  # Retrieve the rating field

        if not name:
            msg = 'Please provide a name for your trip'
            self.add_error('name', msg)
        if not location:
            msg = 'Please provide a location'
            self.add_error('location', msg)
        if not description:
            msg = 'No description was provided'
            self.add_error('description', msg)
        if start_date < now:
            msg = 'Start date must be in the future'
            self.add_error('start_date', msg)
        if end_date < now:
            msg = 'End date must be in the future'
            self.add_error('end_date', msg)
        if end_date < start_date:
            msg = 'End date must be after start date'
            self.add_error('end_date', msg)

        # Add validation for the rating field if needed

        return cleaned_data
