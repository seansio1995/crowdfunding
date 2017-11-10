from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, GroupForm, AddUser, SuspendUser, unSuspendUser
from django.contrib.auth.models import User,Group
from .models import Report
from django.contrib.auth.decorators import login_required



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
                user.save()
            else:
                user.profile.is_company = False
                user.save()
            login(request, user)
            return redirect('userhome')
    else:
        form = SignUpForm
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def report_list(request):
    #this needs to be edited to check for company or investor user
        #if company, only see your own companies' reports
        #if investor, you can see all reports by all companies
    if request.user.profile.is_manager == True:
        reports = Report.objects.all()
        if len(reports) == 0:
            has_rep = False
        else:
            has_rep = True
        return render(request, 'reportsM.html',{'report_list':reports, 'reports':has_rep})
    else:
        reports = Report.objects.filter(created_by = request.user)
        if len(reports) == 0:
            has_rep = False
        else:
            has_rep = True
        return render(request, 'reports.html', {'report_list': reports, 'reports':has_rep})


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
            if user.profile.is_suspended == True:
                return redirect('index')
            login(request,user)
            if user.profile.is_manager == True:
                return render(request, 'manager_home.html')
            else:
                return render(request, 'user_home.html')
        else:
            return render(request, 'index.html')
    else:
        form1 = LoginForm
        return render(request, 'login.html', {'form1':form1})

@login_required(login_url='login')
def createreport(request):
    #also need to check if request.user.profile.is_company is true. Investor users don't create reports
    #need to actually create a report model instance
    #don't forget to set report.created_by to request.user
    if(request.user.profile.is_manager == True):
        return render(request,'createreportM.html')
    else:
        return render(request, 'createreport.html')
    if(request.user.profile.is_company == True):
        return render(request, 'user_home.html')
    else:
        return render (request, 'investor_home.html')



@login_required(login_url = 'login')
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        Group.objects.get_or_create(name=group_name)
        g = Group.objects.get(name= group_name)
        g.user_set.add(request.user)
        g.save()
        if request.user.profile.is_manager == True:
            return redirect('managerhome')
        else:
            return redirect('userhome')
    else:
        form1 = GroupForm
        if request.user.profile.is_manager == True:
            return render(request, 'creategroupM.html', {'form1': form1})
        else:
            return render(request, 'creategroup.html', {'form1': form1})


@login_required(login_url='login')
def group_list(request):
    if request.user.profile.is_manager == False:
        groups = request.user.groups.all()
        if len(groups) == 0:
            has_group = False
        else:
            has_group = True
        return render(request, 'group_list.html',{'groups':groups,'has_group':has_group})
    else:
        groups = Group.objects.all()
        if len(groups) == 0:
            has_group = False
        else:
            has_group = True
        return render(request, 'group_listM.html', {'groups': groups, 'has_group': has_group})


@login_required(login_url='login')
def add_user_to_group(request):
    #managers can add to any group, users only to groups they are in
    if request.user.profile.is_manager:
        if request.method == 'POST':
            username = request.POST.get('username')
            group_name = request.POST.get('group_name')
        else:
            form1 = AddUser
            return render(request, 'add_to_groupM.html', {'form1': form1})

        group = Group.objects.get(name = group_name)
        group.user_set.add(User.objects.get(username=username))
        group.save()
        return redirect('managerhome')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            group_name = request.POST.get('group_name')
        else:
            form1 = AddUser
            return render(request, 'add_to_group.html', {'form1': form1})
        group = Group.objects.get(name = group_name)
        if (request.user not in group.user_set.all()):
            return redirect('add-error')
        else:
            group.user_set.add(User.objects.get(username=username))
            group.save()
            return redirect('userhome')


@login_required(login_url='login')
def user_home(request):
    #needs to be edited to differentiate between investor and company user home page
        #user_home.html is company
        #investor_home.html is investor
    return render(request, 'user_home.html')


@login_required(login_url='login')
def manager_home(request):
    return render(request,'manager_home.html')


@login_required(login_url='login')
def add_SM(request):
    if request.method == 'POST':
        user = User.objects.get(username = request.POST.get('username'))
        user.profile.is_manager = True
        user.save()
        return redirect('managerhome')
    else:
        form1 = SuspendUser
        return render(request, 'add_SM.html', {'form1': form1})


@login_required(login_url='login')
def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        group_name = request.POST.get('group_name')
    else:
        form1 = AddUser
        return render(request, 'delete_user.html', {'form1': form1})

    group = Group.objects.get(name = group_name)
    group.user_set.add(User.objects.remove(username=username))
    group.save()
    return redirect('managerhome')


@login_required(login_url='login')
def add_error(request):
    #all you need here
    return render(request, 'add_user_error.html')

@login_required(login_url='login')
def suspend_user(request):
    #set user's is_suspended to true
    if request.method == 'POST':
        user = User.objects.get(username = request.POST.get('username'))
        user.profile.is_suspended = True
        user.save()
        return redirect('managerhome')
    else:
        form1 = SuspendUser
        return render(request, 'suspend_user.html', {'form1': form1})

@login_required(login_url='login')
def messaging(request):
    #for viewing sent messages and chosing to send a new one
    #not yet implemented
    return render(request, 'messaging.html')

@login_required(login_url='login')
def unsuspend_user(request):
    #set user's is_suspended to true
    if request.method == 'POST':
        user = User.objects.get(username = request.POST.get('username'))
        user.profile.is_suspended = False
        user.save()
        return redirect('managerhome')
    else:
        form1 = unSuspendUser
        return render(request, 'unsuspend_user.html', {'form1': form1})
