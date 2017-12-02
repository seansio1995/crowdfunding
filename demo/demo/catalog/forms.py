from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Report
from simple_search import search_form_factory

from .models import Message, project

from multiupload.fields import MultiFileField


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    user_type = forms.MultipleChoiceField(
        required = True,
        widget = forms.RadioSelect(),
        choices = [("company","company"),("investor","investor")]
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type' )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, required=True)

class GroupForm(forms.Form):
    group_name = forms.CharField(max_length=30, required=True)

class AddUser(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    group_name = forms.CharField(max_length=30, required=True)

class SuspendUser(forms.Form):
    username = forms.CharField(max_length=30, required=True)

class unSuspendUser(forms.Form):
    username = forms.CharField(max_length=30, required=True)


class MessageForm(forms.Form):
    receiver = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'max_length': 255}))
    message = forms.CharField(widget=forms.Textarea)
    encrypt = forms.BooleanField(required=False)

class DeleteMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = []


class ProjectForm(forms.Form):
    companyname = forms.CharField(max_length=30, required=True)
    projectname = forms.CharField(max_length=30, required=True)
    description = forms.CharField(max_length=1000, required=True)


ReportSearchForm = search_form_factory(Report.objects.all(),
                                 ['^company',
                                  'sector',
                                  'current_projects',
                                  'location',
                                  'country',
                                  'industry',
                                  'description',
                                  'funding_goal',
                                  'timestamp'])

ProjectSearchForm = search_form_factory(project.objects.all(),
                                 ['^project_name',
                                  'project_description',
                                  'project_company'
                                        ])


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class reportRateForm(forms.Form):

    CHOICES=[(i,i) for i in range(11)]

    office = forms.MultipleChoiceField(
            choices=CHOICES,
            widget=forms.SelectMultiple(),
            required=True,
            label='Ratings',
        )

class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    #attachments = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)
    
