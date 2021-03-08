from django import forms
from django.forms import DateInput

from .models import Posts

class DocumentForm(forms.ModelForm):


    post_name = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'post_name'}),
        required=True,
    )

    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'id': 'start'}, ),
        required=False,
    )

    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'id': 'end'}),
        required=False,
    )

    description = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'description'}),
        required=True,
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'location'}),
        required=False,
    )

    type = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'type'}),
        required=True,
        initial="Default"
    )

    attendees_min = forms.IntegerField(
        label='Select a file',
        required=False,
        widget=forms.NumberInput(attrs={'id': 'attendees_min'}),
        initial = 0
    )

    attendees_max = forms.IntegerField(
        label='Select a file',
        required=False,
        widget=forms.NumberInput(attrs={'id': 'attendees_max'}),
        initial=0
    )

    image = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required=False,
        widget=forms.FileInput(attrs={'id': 'image'}),
    )



    class Meta:
        model = Posts
        fields = ("post_name", "group", "start", "end", "location", "description", "attendees_min", "attendees_max", "image", "type")
