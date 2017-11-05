from .models import Person, Friend
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# Create your views here.

def index(request):
    num_peeps = Person.objects.all().count()
    num_frens = Friend.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_peeps':num_peeps,'num_frens':num_frens},
    )




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
