from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, GroupForm, AddUser
from django.contrib.auth.models import User,Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Report






def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if 'company' in request.POST:
                user.profile.is_company = True
            else:
                user.profile.is_company = False
            user.profile.is_manager = True
            login(request, user)
            return redirect('userhome')
    else:
        form = SignUpForm
    return render(request, 'signup.html', {'form': form})


def report_list(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            if request.user.is_manager == True:
                reports = Report.objects.all()
                if len(reports) == 0:
                    has_rep = False
                else:
                    has_rep = True
                return render(request, 'reports.html',{'report_list':reports, 'reports':has_rep})
            else:
                reports = Report.objects.filter(created_by = request.user)
                if len(reports) == 0:
                    has_rep = False
                else:
                    has_rep = True
                return render(request, 'reports.html', {'report_list': reports, 'reports':has_rep})
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
            user = authenticate(username = request.POST.get('username'),password = request.POST.get('password'))
            login(request,user)
            request.session['logged'] = True
            if user.profile.is_manager == True:
                return render(request, 'manager_home.html')
            else:
                return render(request, 'user_home.html')
        else:
            return render(request, 'index.html')
    else:
        form1 = LoginForm
        return render(request, 'login.html', {'form1':form1})


def createreport(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            #need to actually create a report model instance
            #don't forget to set report.created_by to request.user
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

def create_group(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            if request.method == 'POST':
                group_name = request.POST.get('group_name')
                Group.objects.get_or_create(name=group_name)
                g = Group.objects.get(name= group_name)
                g.user_set.add(request.user)
                return redirect('group')
            else:
                form1 = GroupForm
                return render(request, 'creategroup.html', {'form1': form1})

        else:
            return redirect('login')
    else:
        return redirect('login')

def group(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            return render(request, 'group.html')
        else:
            return redirect('login')
    else:
        return redirect('login')

def group_list(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            if request.user.is_manager == False:
                groups = request.user.groups.all()
                if len(groups) == 0:
                    has_group = False
                else:
                    has_group = True
                return render(request, 'group_list.html',{'groups':groups,'has_group':has_group})
            else:
                groups = User.objects.groups.all()
                if len(groups) == 0:
                    has_group = False
                else:
                    has_group = True
                return render(request, 'group_list.html', {'groups': groups, 'has_group': has_group})
        else:
            return redirect('login')
    else:
        return redirect('login')

def add_user_to_group(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            if request.method == 'POST':
                username = request.POST.get('username')
                group_name = request.POST.get('group_name')
            else:
                form1 = AddUser
                return render(request, 'group.html', {'form1': form1})

            group = Group.objects.get(name = group_name)
            group.user_set.add(User.objects.get(username=username))
        else:
            return redirect('login')
    else:
        return redirect('login')


def loggedin(request):
    if 'logged' in request.session:
        if request.session['logged'] == True:
            if request.user.is_manager == True:
                return redirect(request,'manager_home.html')
            else:
                return render(request, 'user_home.html')
        else:
            return redirect('login')
    else:
        return redirect('login')

def add_SM(request):
    return render(request, 'add_SM.html')