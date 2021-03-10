from django import forms
from .models import *
from django.db import connection
from .models import Posts


class PostForm(forms.ModelForm):
    """
    Class PostForm to display and handle the new post form
    """

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
        widget=forms.Textarea(attrs={'id': 'description', 'size': 1950,
                                     'maxlength': 1950}),required=True,
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
        help_text='max. 10 megabytes',
        required=False,
        widget=forms.FileInput(attrs={'id': 'image'}),
    )

    def __init__(self, *args, **kwargs):
        # Get the list of communities the user is in

        self.user_id = kwargs.pop('user_id')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM members WHERE user_id=%s", (self.user_id,))
            data = cursor.fetchall()

        # Get the community IDs and store in list
        group_list = []
        for i in data:
            group_list.append(i[2])

        # Get communities
        self.groups = UniGroups.objects.filter(group_id__in=group_list)

        super(PostForm, self).__init__(*args, **kwargs)

        # Set the group field in the form to be a dropdown list
        # of all the enrolled communities
        self.fields['group'].queryset = self.groups



    class Meta:
        model = Posts
        fields = ("post_name", "group", "start", "end", "location", "description",
                  "attendees_min", "attendees_max", "image", "type")


class ProfilePicForm(forms.ModelForm):
    """
    Class ProfilePicForm to display and handle the update profile picture form
    """

    image = forms.FileField(
        widget = forms.FileInput(attrs={"id":"image"})

    )
    class Meta:
        model = Pics
        fields = ("pic",)