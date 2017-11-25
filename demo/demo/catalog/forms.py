from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages

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

class ProjectForm(forms.Form):
    companyname = forms.CharField(max_length=30, required=True)
    projectname = forms.CharField(max_length=30, required=True)
    description = forms.CharField(max_length=1000, required=True)
