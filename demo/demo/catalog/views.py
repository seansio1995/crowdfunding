from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import FileUploadForm,ImageUploadForm, SignUpForm, LoginForm, GroupForm, AddUser, SuspendUser, unSuspendUser,MessageForm, ProjectForm, DeleteMessage,CommentForm

from django.contrib.auth.models import User,Group
from .models import Report, Message,KeyPair, project,comment,file
from django.contrib.auth.decorators import login_required


from .forms import DeleteMessage
from .models import Message

from django.http import HttpResponseRedirect, HttpResponse


from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import Crypto
from ast import literal_eval
from tagging.models import Tag, TaggedItem

import operator
from .forms import ReportSearchForm, ProjectSearchForm
from .forms import reportRateForm
from .models import reportRate


from geopy.geocoders import Nominatim


import re
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_type=request.POST.get("user_type")
            user = authenticate(username=username, password=raw_password)
            random_generator = Random.new().read
            RSAkey=RSA.generate(1024,random_generator).exportKey()
            pubkey=RSA.importKey(RSAkey).publickey().exportKey()
            keypair = KeyPair.objects.create(
                user=user,RSAkey=RSAkey,pubkey=pubkey
            )

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
    #return HttpResponse("Hello, world.  You're at the catalog index.")
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
    report=Report.objects.get(pk=pk)
    current_rate=0
    if request.method=="POST" and "post_comment" in request.POST:
        form=CommentForm(request.POST)
        if form.is_valid():
            comment_content=form.cleaned_data["comment"]
            comment.objects.create(sender_name=request.user.username,comment=comment_content,report_id=pk)
    elif request.method=="POST" and "delete-comment" in request.POST:
        print("delete-comment" in request.POST)
        comment_id=request.POST.get("comment_id")
        print(comment_id)
        comment_delete=comment.objects.get(id=comment_id)
        comment_delete.delete()
    elif request.method=="POST" and "rate" in request.POST:
        print(request.POST.get("dropdown"))
        rate=float(request.POST.get("dropdown"))
        current_rate=rate
        reportRate.objects.create(report_rate=rate,rate_by=request.user.username,report_id=pk)
        # rateForm=reportRateForm(request.POST)
        # if rateForm.is_valid():
        #     print(rateForm.cleaned_data["value"])
    #commentform=CommentForm(request.POST)
    elif request.method=="POST" and "favorite_report" in request.POST:
        report.is_favorite=True
        report.save()
    elif request.method=="POST" and "unfavorite_report" in request.POST:
        report.is_favorite=False
        report.save()

    reportRates=reportRate.objects.filter(report_id=pk)
    totalRate=0
    count=0
    for r in reportRates:
        totalRate+=r.report_rate
        count+=1
    if count!=0:
        average_rate=totalRate/count
    else:
        average_rate=0
    report.average_rate=average_rate
    report.save()
    average_rate_format=format(report.average_rate, '.3f')
    comments=comment.objects.filter(report_id=pk)
    geolocator = Nominatim()
    location = geolocator.geocode(report.location)
    print(location.latitude)
    print(location.longitude)
    return render(request,'view_report.html',{
    "report":report,"location":location,"commentform":CommentForm(),"comments":comments,"averageRate":average_rate_format,"currentRate":current_rate
})


@login_required(login_url = 'login')
def viewallreport(request):
    search_key = request.POST.get('myList')
    #print(search_key)
    search_val = request.POST.get('search_val')
    #report = get_object_or_404(Report)

    if request.method == 'POST' and "delete-report" in request.POST:
        #form = DeleteMessage(request.POST, instance=message)
        print("delete-report" in request.POST)
        #if form.is_valid(): # checks CSRF
        reportpk= request.POST.get("report_id")
        print(reportpk)
        report = Report.objects.get(pk=reportpk)
        report.delete()
        #message.save()
        #return HttpResponseRedirect("deletemessage.html") # wherever to go after deleting
        return render(
                 request,
                 'delete_report.html'
              )

    else:
        search_val = searchreport(request)
        if search_val is None:
           report_list=Report.objects.all()
        else:
        #    options = {}
        #    options[search_key] = search_val
           report_list=Report.objects.filter(search_val)
        #report=Report.objects.all()[0]
        return render(request,'view_all_report.html',{
        "report_list":report_list})

def searchreport(request):
    queries = []
    operator = request.POST.get('operator')
    keys = ['company', 'sector', 'industry', 'location', 'country', 'projects']
    q = None
    for k in keys:
        if request.POST.get(k) != "":
           if q is None:
              q = Q()
           options = {}
           options[k] = request.POST.get(k)
           if operator == "and":
                q = q & Q(**options)
           elif operator == "or":
                q = q | Q(**options)
           else:
                q = None
    return q




@login_required(login_url = 'login')
def viewgroup(request,pk):
    if request.user.profile.is_manager == True:
        group = Group.objects.get(pk=pk)
        users = group.user_set.all()
        return render(request, 'group_membersM.html', {'users': users})
    else:
        group = Group.objects.get(pk=pk)
        users = group.user_set.all()
        return render(request,'group_members.html',{'users':users})



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
            encrypt=form.cleaned_data['encrypt']
            content=""
            if encrypt:
                user = User.objects.get(username=receiver)
                receiver_keypair=KeyPair.objects.get(user=user).RSAkey.encode('utf-8')
                src_data=message
                receiver_pubkey=RSA.importKey(KeyPair.objects.get(user=user).pubkey)
                enc_data = receiver_pubkey.encrypt(src_data.encode(), 32)[0]
                message=str(enc_data)
                content="The message is encrypted"
            message = Message.objects.create(
                    message=message, content=content,sender=sender,receiver=receiver,encrypt=encrypt)
            return render(request,"send_message_success.html")
    else:
        return render(
                request,
                'send_message.html',
                {'form': MessageForm()})




def send_group_message(request):
    if request.method=="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            sent_message = form.cleaned_data['message']
            group_receiver= (form.cleaned_data['receiver']).strip()
            sender = request.user.username
            encrypt=form.cleaned_data['encrypt']
            g=Group.objects.get(name=group_receiver)
            users = g.user_set.all()
            sent_content=""
            for user in users:
                print(user.username)
                tmp_message=sent_message
                if encrypt:
                    receiver_keypair=KeyPair.objects.get(user=user).RSAkey.encode('utf-8')
                    src_data=sent_message
                    receiver_pubkey=RSA.importKey(KeyPair.objects.get(user=user).pubkey)
                    enc_data = receiver_pubkey.encrypt(src_data.encode(), 32)[0]
                    tmp_message=str(enc_data)
                    sent_content="The message is encrypted"
                message = Message.objects.create(
                        message=tmp_message, content=sent_content,sender=sender,receiver=user.username,encrypt=encrypt)
            return render(request,"send_message_success.html")
    else:
        return render(
                request,
                'send_message.html',
                {'form': MessageForm()})





#@csrf_protect
def receive_message(request):
    if request.method=="POST" and "send-message" in request.POST:
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            receiver= (form.cleaned_data['receiver']).strip()
            encrypt=form.cleaned_data['encrypt']
            sender = request.user.username
            encrypt=form.cleaned_data['encrypt']
            if encrypt:
                user = User.objects.get(username=receiver)
                src_data=message
                receiver_pubkey=RSA.importKey(KeyPair.objects.get(user=user).pubkey)
                enc_data = receiver_pubkey.encrypt(src_data.encode(), 32)[0]
                message=str(enc_data)
                content="The message is encrypted"
            message = Message.objects.create(
                    message=message, content=content, sender=sender,receiver=receiver,encrypt=encrypt)
            messages = Message.objects.filter(receiver=request.user.username)

            return render(
                    request,
                    'receive_message.html',
                    {'messages': messages,'form':MessageForm()}
                )
        else:
            print("NOT VALID")
    elif request.method=="POST" and "decrypt-message" in request.POST:
        print(request.POST.get('message_id'))
        message_id=request.POST.get('message_id')
        form = MessageForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['message'])
        message = Message.objects.get(id=message_id)
        if message.encrypt:
            print("find message!")
            user = User.objects.get(username=request.user.username)
            receiver_keypair=KeyPair.objects.get(user=user).RSAkey
            privkey = RSA.importKey(receiver_keypair)
            message.message=privkey.decrypt(eval(message.message)).decode()
            message.encrypt=False
            message.save()
        else:
            messages = Message.objects.filter(receiver=request.user.username)
            return render(
                    request,
                    'decrypt_message_error.html',
                    {'messages': messages,'form':MessageForm()}
                )

        messages = Message.objects.filter(receiver=request.user.username)

        return render(
                request,
                'receive_message.html',
                {'messages': messages,'form':MessageForm()}
            )
    elif request.method == 'POST' and "delete-message" in request.POST:
        #form = DeleteMessage(request.POST, instance=message)
        print("delete-message" in request.POST)
        #if form.is_valid(): # checks CSRF
        messagepk= request.POST.get("messagepk")
        message = Message.objects.get(id=messagepk)
        message.delete()
        return render(
                 request,
                 'deletemessage.html'
              )
    messages = Message.objects.filter(receiver=request.user.username)
    return render(
            request,
            'receive_message.html',
            {'messages': messages,'form':MessageForm()}
        )



def gohome(request):
    if request.user.profile.is_manager == True:
        return render(request,"manager_home.html")
    elif request.user.profile.is_company:
        return render(request,"user_home.html")
    else:
        return render(request,"investor_home.html")

def project_list(request):
    try:
        has_project = True
        tags = Tag.objects.get(name = request.user.username)
        Projects = TaggedItem.objects.get_by_model(project,tags)
    except:
        has_project = False
        Projects = []
    return render(request, 'project_list.html', {'projects': Projects, 'has_project': has_project})


def add_project(request,pk):
    Project = project.objects.get(pk=pk)
    Tag.objects.add_tag(Project,request.user.username)
    return redirect('projects')


def upvote_project(request,pk):
    Project = project.objects.get(pk=pk)
    Project.upvotes = Project.upvotes + 1
    Project.save()
    return redirect('gohome')

def project_list_all(request):
    projects = project.objects.all()
    if len(projects) == 0:
        has_project = False
    else:
        has_project = True
    return render(request, 'all_projects.html', {'projects': projects, 'has_project': has_project})

def create_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('projectname')
        company_name = request.POST.get('companyname')
        description = request.POST.get('description')
        project.objects.get_or_create(project_name = project_name)
        p = project.objects.get(project_name= project_name)
        p.company_name = company_name
        p.description = description
        p.save()
        return redirect('gohome')
    else:
        form1 = ProjectForm
        return render(request, 'createproject.html', {'form1': form1})

# class ReportSearchListView(ReportListView):
#
#     paginate_by = 10
#
#     def get_queryset(self):
#         result = super(ReportSearchListView, self).get_queryset()
#
#         query = self.request.GET.get('r')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Report(company__icontains=r) for r in query_list))
#             )
#
#         return result


def report_search(request):
    form = ReportSearchForm(request.GET or {})
    if form.is_valid():
        results = form.get_queryset()
    else:
        results = Report.objects.none()
    if request.method=="POST" and "sort_rate" in  request.POST:
        results=Report.objects.order_by("-average_rate")
    return render(request, 'report_search.html',{
        'form':form,
        'results':results
    })

def project_search(request):
    form = ProjectSearchForm(request.GET or {})
    if form.is_valid():
        results = form.get_queryset()
    else:
        results = project.objects.none()
    if request.method=="POST" and "sort_vote" in request.POST:
        results=project.objects.order_by("-upvotes")
    return render(request, 'project_search.html',{
        'form':form,
        'results':results
    })

def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = User.objects.get(username=request.user.username)
            m.profile.avatar = form.cleaned_data['image']
            m.save()
            return redirect('gohome')
    else:
        return render(request,'upload_pic.html')

def upload_file(request,pk):
    rep = Report.objects.get(pk=pk)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #rep = Report.objects.get(pk=pk)
            rep.files = file.objects.create(file=form.cleaned_data['file'])
            rep.save()
            return redirect("viewallreport")
    # else:
    #     form=FileUploadForm()
    # documents=file.objects.all()
    # return render(request,"view_report.html",{"documents":documents,"form":form})
def list_favorite_report(request):
    if request.method=="POST" and "unfavorite_report" in request.POST:
        reportpk= request.POST.get("report_id")
        report=Report.objects.get(pk=reportpk)
        report.is_favorite=False
        report.save()
    search_key = request.POST.get('myList')
    search_val = request.POST.get('search_val')
    if search_val is None:
       report_list=Report.objects.filter(is_favorite=True)
    else:
       options = {}
       options[search_key] = search_val
       report_list=Report.objects.filter(**options)
       report_list=report_list.filter(is_favorite=True)
    #report=Report.objects.all()[0]
    return render(request,'listfavoritereport.html',{
    "report_list":report_list})
