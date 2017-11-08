from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    user_type = forms.MultipleChoiceField(
        required = True,
        widget = forms.RadioSelect(),
        choices = (("Company","company"),("Investor","investor"))
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