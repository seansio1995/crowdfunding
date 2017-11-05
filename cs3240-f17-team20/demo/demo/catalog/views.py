from django.shortcuts import render
from .models import Person, Friend
# Create your views here.

def index(request):
    num_peeps = Person.objects.all().count()
    num_frens = Friend.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_peeps':num_peeps,'num_frens':num_frens},
    )