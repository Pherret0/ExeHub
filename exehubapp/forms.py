from django import forms
from django.forms import DateInput
from .models import *
from django.db import connection
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


    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM members WHERE user_id=%s", (str(self.user_id)), )
            data = cursor.fetchall()

        group_list = []
        for i in data:
            group_list.append(i[1])

        self.groups = UniGroups.objects.filter(group_id__in=group_list)
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = self.groups



    class Meta:
        model = Posts
        fields = ("post_name", "group", "start", "end", "location", "description", "attendees_min", "attendees_max", "image", "type")

class ProfilePicForm(forms.ModelForm):
    image = forms.FileField(
        widget = forms.FileInput(attrs={"id":"image"}))
    class Meta:
        model = Pics
        fields = ("pic",)