from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
# Create your views here.


##!!!! if you add a view, make sure to add the @login_required tag before so that it cannot be accessed
    #just by typing in the url!!!!!

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('signup.html')
    else:
        form = SignUpForm
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='login')
def report_list(request):
    return render(request, 'reports.html')

def index(request):
    return render(
        request,
        'index.html',
        context={},
    )

def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid() is True:
            return render(request, 'user_home.html')
        else:
            return render(request, 'index.html')
    else:
        form1 = LoginForm
        return render(request, 'login.html', {'form1':form1})


def logout(request):
    return render(request, 'logged_out.html')

@login_required(login_url="login")
def createreport(request):
    if request.method=="POST":
        return redirect("index")
    return render(request,'createreport.html')

@login_required(login_url="login")
def messaging(request):
    return render(request, 'messaging.html')

@login_required(login_url="login")
def loggedin(request):
    return render(request,'user_home.html')