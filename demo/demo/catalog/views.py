from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm, GroupForm, AddUser, SuspendUser, unSuspendUser,MessageForm, DeleteMessage
from django.contrib.auth.models import User,Group
from .models import Report, Message
from django.contrib.auth.decorators import login_required

from .forms import DeleteMessage
from .models import Message


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            #user_type=form.cleaned_data["user_type"]
            #reason = form.cleaned_data['reason']
            #user_type = dict(form.fields['user_type'].choices)[user_type]
            user_type=request.POST.get("user_type")
            user = authenticate(username=username, password=raw_password)
            if user_type=="company":
                user.profile.is_company = True
                user.save()
            else:
                user.profile.is_investor = True
                user.save()
            login(request, user)
            return redirect('gohome')
    else:
        form = SignUpForm
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def report_list(request):
    if request.user.profile.is_manager == True or request.user.profile.is_company == False:
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
            elif user.profile.is_company == True :
                return render(request, 'user_home.html')
            else:
                return render(request,'investor_home.html')

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
    if request.user.profile.is_manager == True or request.user.profile.is_company == True:
        if request.method=="POST":
            r=Report()
            #r.init_date=request.POST['init_date']
            r.current_projects=request.POST.get('current_projects')
            r.company=request.POST.get('company')
            r.phone=request.POST.get('phone')
            r.location=request.POST.get('location')
            r.country=request.POST.get('country')
            r.sector=request.POST.get('sector')
            r.industry=request.POST.get('industry')
            r.description=request.POST.get('description')
            # r.report_no=request.POST('report_no')
            r.save()
            return render(request,'report_success.html')
        return render(request,'createreportM.html')

    # elif(request.user.profile.is_company == True):
    #     if request.method == 'POST':
    #         return render(request,"report_success.html")
    #     return render(request, 'createreport.html',{})
        #return render(request, 'user_home.html')
    # else:
    #     return render (request, 'investor_home.html')

@login_required(login_url = 'login')
def edit_report(request, pk):
    r = Report.objects.get(pk=pk)
    return render(request, 'edit_report.html', {'report':r})

@login_required(login_url='login')
def finish_edit(request, pk):
    r = Report.objects.get(pk=pk)
    r.current_projects = request.POST.get('current_projects')
    r.company = request.POST.get('company')
    r.phone = request.POST.get('phone')
    r.location = request.POST.get('location')
    r.country = request.POST.get('country')
    r.sector = request.POST.get('sector')
    r.industry = request.POST.get('industry')
    r.description = request.POST.get('description')
    r.save()
    return render(request, 'report_success.html')


@login_required(login_url = 'login')
def viewreport(request,pk):
    #report = get_object_or_404(Report)
    report=Report.objects.get(pk=pk)
    return render(request,'view_report.html',{
    "report":report
})


@login_required(login_url = 'login')
def viewallreport(request):
    #Not implemented yet
    #report = get_object_or_404(Report)
    report_list=Report.objects.all()
    #report=Report.objects.all()[0]
    return render(request,'view_all_report.html',{
    "report_list":report_list
})



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
    group.user_set.remove(User.objects.get(username=username))
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


#@csrf_protect
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            receiver= (form.cleaned_data['receiver']).strip()
            sender = request.user.username
            message = Message.objects.create(
                    message=message, sender=sender,receiver=receiver)
            return render(request,"send_message_success.html")
    else:
        return render(
                request,
                'send_message.html',
                {'form': MessageForm()})

    #####
    
#def deletemessage(request, pk):
  #  if request.method == 'POST':
  #      message = Message.objects.get(pk=pk)
  #      message.delete()
  #      return render(request,'deletemessage.html')    
    
    #### post a  rpimary key, message.object.get (pk==pk) , message.delete(), return a response to deletemsg.html
    #### make a form for delete 
#@csrf_protect
def deletemessage(request):
   #message = Message.objects.get(pk=pk)
   if request.method == 'POST' and "delete-message" in request.POST:
        #form = DeleteMessage(request.POST, instance=message)

        #if form.is_valid(): # checks CSRF
        messagepk= request.POST.get("messagepk")
        message = Message.objects.get(id=messagepk)
        message.delete()
        #message.save()
        return HttpResponseRedirect("deletemessage.html") # wherever to go after deleting

   else:
        form = DeleteMessage(instance=message)
   
        template_vars = {'form': form}
        return render(request, 'deletemessage.html', template_vars)
    
    
    
#def deletemessage(request, pk, template_name='deletemessage.html'):
 #   message = get_object_or_404(Message, pk=pk)    
  #  if request.method=='POST':
   #     message.delete()
    #    return redirect('deletemessage.html')
    #return render(request, template_name, {'form':form})    
   
###

#@csrf_protect
def receive_message(request):
    if request.method=="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            receiver= (form.cleaned_data['receiver']).strip()
            sender = request.user.username
            message = Message.objects.create(
                    message=message, sender=sender,receiver=receiver)
            messages = Message.objects.filter(receiver=request.user.username)
            return render(
                    request,
                    'receive_message.html',
                    {'messages': messages,'form':MessageForm()}
                )

    messages = Message.objects.filter(receiver=request.user.username)
    return render(
            request,
            'receive_message.html',
            {'messages': messages,'form':MessageForm()}
        )

#@csrf_protect
def receivemessage(request):
    if request.method=="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            receiver= (form.cleaned_data['receiver']).strip()
            sender = request.user.username
            message = Message.objects.create(
                    message=message, sender=sender,receiver=receiver)
            messages = Message.objects.filter(receiver=request.user.username)
            return render(
                    request,
                    'receivemessage.html',
                    {'messages': messages,'form':MessageForm()}
                )

    messages = Message.objects.filter(receiver=request.user.username)
    return render(
            request,
            'receivemessage.html',
            {'messages': messages,'form':MessageForm()}
        )
    if request.method == 'POST' and "delete-message" in request.POST:
        #form = DeleteMessage(request.POST, instance=message)
        print("delete-message" in request.POST)
        #if form.is_valid(): # checks CSRF
        messagepk= request.POST.get("messagepk")
        message = Message.objects.get(id=messagepk)
        message.delete()
        #message.save()
        return HttpResponseRedirect("deletemessage.html") # wherever to go after deleting

    
def gohome(request):
    if request.user.profile.is_manager == True:
        return render(request,"manager_home.html")
    elif request.user.profile.is_company:
        return render(request,"user_home.html")
    else:
        return render(request,"investor_home.html")
