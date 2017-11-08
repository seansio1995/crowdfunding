from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
# Create your views here.





def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if 'Company' in request.POST:
                user.is_company = True
            else:
                user.is_company = False
            return redirect('userhome')
    else:
        form = SignUpForm
    return render(request, 'signup.html', {'form': form})


def report_list(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            return render(request, 'reports.html')
        else:
            return redirect('login')
    else:
        return redirect('login')

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
            request.session['logged'] = True
            return render(request, 'user_home.html')
        else:
            return render(request, 'index.html')
    else:
        form1 = LoginForm
        return render(request, 'login.html', {'form1':form1})


def createreport(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            return render(request, 'createreport.html')
        else:
            return redirect('login')
    else:
        return redirect('login')



def messaging(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            return render(request, 'messaging.html')
        else:
            return redirect('login')
    else:
        return redirect('login')

def logout(request):
    request.session['logged'] = False
    return render(request, 'logged_out.html')

def loggedin(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            return render(request, 'user_home.html')
        else:
            return redirect('login')
    else:
        return redirect('login')

