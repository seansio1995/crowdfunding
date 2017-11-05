from django.shortcuts import render
from django.views import generic
from .models import Person, Friend, Report
# Create your views here.

def index(request):
    num_peeps = Person.objects.all().count()
    num_frens = Friend.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_peeps':num_peeps,'num_frens':num_frens},
    )

class ReportListView(generic.ListView):
    model = Report