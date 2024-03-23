import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from module.forms import AddEmployeeForm, EditEmployeeForm
from module.models import CustomUser, TL, Project, Client, Employee, SessionYearModel, \
    FeedBackEmployee, FeedBackTL, LeaveReportEmployee, LeaveReportTL, Attendance, AttendanceReport, \
    NotificationEmployee, NotificationTL


def manager_home(request):
    employee_count=Employee.objects.all().count()
    tl_count=TL.objects.all().count()
    client_count=Client.objects.all().count()
    project_count=Project.objects.all().count()

    project_all=Project.objects.all()
    project_name_list=[]
    client_count_list=[]
    employee_count_list_in_project=[]
    for project in project_all:
        client=Client.objects.filter(project_id=project.id).count()
        employee=Employee.objects.filter(project_id=project.id).count()
        project_name_list.append(project.project_name)
        client_count_list.append(client)
        employee_count_list_in_project.append(employee)

    client_all=Client.objects.all()
    client_list=[]
    employee_count_list_in_client=[]
    for clients in client_all: 
        project=Project.objects.get(id=clients.project_id.id)
        employee_count=Employee.objects.filter(project_id=project.id).count()
        client_list.append(clients.client_name)
        employee_count_list_in_client.append(employee_count)

    tl=TL.objects.all()
    attendance_present_list_tl=[]
    attendance_absent_list_tl=[]
    tl_name_list=[]
    for t in tl:
        client_ids=Client.objects.filter(TL_id=t.admin.id)
        attendance=Attendance.objects.filter(client_id__in=client_ids).count()
        leaves=LeaveReportTL.objects.filter(TL_id=t.id,leave_status=1).count()
        attendance_present_list_tl.append(attendance)
        attendance_absent_list_tl.append(leaves)
        tl_name_list.append(t.admin.username)

    employee_all=Employee.objects.all()
    attendance_present_list_employee=[]
    attendance_absent_list_employee=[]
    employee_name_list=[]
    for employeee in employee_all:
        attendance=AttendanceReport.objects.filter(employee_id=employeee.id,status=True).count()
        absent=AttendanceReport.objects.filter(employee_id=employeee.id,status=False).count()
        leaves=LeaveReportEmployee.objects.filter(employee_id=employeee.id,leave_status=1).count()
        attendance_present_list_employee.append(attendance)
        attendance_absent_list_employee.append(leaves+absent)
        employee_name_list.append(employeee.admin.username)


    return render(request,"manager_template/home_content.html",{"employee_count":employee_count,"tl_count":tl_count,"client_count":client_count,"project_count":project_count,"project_name_list":project_name_list,"client_count_list":client_count_list,"employee_count_list_in_project":employee_count_list_in_project,"employee_count_list_in_client":employee_count_list_in_client,"client_list":client_list,"tl_name_list":tl_name_list,"attendance_present_list_tl":attendance_present_list_tl,"attendance_absent_list_tl":attendance_absent_list_tl,"employee_name_list":employee_name_list,"attendance_present_list_employee":attendance_present_list_employee,"attendance_absent_list_employee":attendance_absent_list_employee})

def add_TL(request):
    return render(request,"manager_template/add_TL_template.html")

def add_TL_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_project(request):
    return render(request,"manager_template/add_project_template.html")

def add_project_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        project=request.POST.get("course")
        try:
            project_model=Project(project_name=project)
            project_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_project"))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_project"))

def add_employee(request):
    form=AddEmployeeForm()
    return render(request,"manager_template/add_employee_template.html",{"form":form})

def add_employee_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddEmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            project_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.employee.address=address
                project_obj=Project.objects.get(id=project_id)
                user.employee.project_id=project_obj
                session_year=SessionYearModel.object.get(id=session_year_id)
                user.employee.session_year_id=session_year
                user.employee.gender=sex
                user.employee.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddEmployeeForm(request.POST)
            return render(request, "manager_template/add_employee_template.html", {"form": form})


def add_client(request):
    project=Project.objects.all()
    tl=CustomUser.objects.filter(user_type=2)
    return render(request,"manager_template/add_client_template.html",{"tl":tl,"project":project})

def add_client_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        client_name=request.POST.get("subject_name")
        project_id=request.POST.get("course")
        project=Project.objects.get(id=project_id)
        tl_id=request.POST.get("staff")
        tl=CustomUser.objects.get(id=tl_id)

        try:
            client=Client(client_name=client_name,project_id=project,TL_id=tl)
            client.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_client"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_client"))


def manage_TL(request):
    tl=TL.objects.all()
    return render(request,"manager_template/manage_TL_template.html",{"tl":tl})

def manage_employee(request):
    employee=Employee.objects.all()
    return render(request,"manager_template/manage_employee_template.html",{"employee":employee})

def manage_project(request):
    project=Project.objects.all()
    return render(request,"manager_template/manage_project_template.html",{"project":project})

def manage_client(request):
    client=Client.objects.all()
    return render(request,"manager_template/manage_client_template.html",{"client":client})

def edit_TL(request,TL_id):
    tl=TL.objects.get(admin=TL_id)
    return render(request,"manager_template/edit_TL_template.html",{"tl":tl,"id":TL_id})

def edit_TL_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        tl_id=request.POST.get("tl_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=tl_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            tl_model=TL.objects.get(admin=tl_id)
            tl_model.address=address
            tl_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_TL",kwargs={"TL_id":tl_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_TL",kwargs={"TL_id":tl_id}))

def edit_employee(request,employee_id):
    request.session['employee_id']=employee_id
    employee=Employee.objects.get(admin=employee_id)
    form=EditEmployeeForm()
    form.fields['email'].initial=employee.admin.email
    form.fields['first_name'].initial=employee.admin.first_name
    form.fields['last_name'].initial=employee.admin.last_name
    form.fields['username'].initial=employee.admin.username
    form.fields['address'].initial=employee.address
    form.fields['project'].initial=employee.project_id.id
    form.fields['sex'].initial=employee.gender
    form.fields['session_year_id'].initial=employee.session_year_id.id
    return render(request,"manager_template/edit_employee_template.html",{"form":form,"id":employee_id,"username":employee.admin.username})

def edit_employee_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id=request.session.get("employee_id")
        if employee_id==None:
            return HttpResponseRedirect(reverse("manage_employee"))

        form=EditEmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            project_id = form.cleaned_data["project"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=employee_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                employee=Employee.objects.get(admin=employee_id)
                employee.address=address
                session_year = SessionYearModel.object.get(id=session_year_id)
                employee.session_year_id = session_year
                employee.gender=sex
                project=Project.objects.get(id=project_id)
                employee.project_id=project
                if profile_pic_url!=None:
                    employee.profile_pic=profile_pic_url
                employee.save()
                del request.session['employee_id']
                messages.success(request,"Successfully Edited Employee")
                return HttpResponseRedirect(reverse("edit_employee",kwargs={"employee_id":employee_id}))
            except:
                messages.error(request,"Failed to Edit Employee")
                return HttpResponseRedirect(reverse("edit_employee",kwargs={"employee_id":employee_id}))
        else:
            form=EditEmployeeForm(request.POST)
            employee=Employee.objects.get(admin=employee_id)
            return render(request,"manager_template/edit_employee_template.html",{"form":form,"id":employee_id,"username":employee.admin.username})

def edit_client(request,client_id):
    client=Client.objects.get(id=client_id)
    project=Project.objects.all()
    tl=CustomUser.objects.filter(user_type=2)
    return render(request,"manager_template/edit_client_template.html",{"client":client,"tl":tl,"project":project,"id":client_id})

def edit_client_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        client_id=request.POST.get("client_id")
        client_name=request.POST.get("client_name")
        tl_id=request.POST.get("staff")
        project_id=request.POST.get("course")

        try:
            client=Client.objects.get(id=client_id)
            client.client_name=client_name
            tl=CustomUser.objects.get(id=tl_id)
            client.tl_id=tl
            project=Project.objects.get(id=project_id)
            client.project_id=project
            client.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_client",kwargs={"client_id":client_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_client",kwargs={"client_id":client_id}))


def edit_project(request,project_id):
    project=Project.objects.get(id=project_id)
    return render(request,"manager_template/edit_project_template.html",{"project":project,"id":project_id})

def edit_project_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        project_id=request.POST.get("project_id")
        project_name=request.POST.get("course")

        try:
            project=Project.objects.get(id=project_id)
            print(Project.project_name)
            project.project_name=project_name
            project.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_project",kwargs={"project_id":project_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_project",kwargs={"project_id":project_id}))


def manage_session(request):
    return render(request,"manager_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def TL_feedback_message(request):
    feedbacks=FeedBackTL.objects.all()
    return render(request,"manager_template/TL_feedback_template.html",{"feedbacks":feedbacks})

def employee_feedback_message(request):
    feedbacks=FeedBackEmployee.objects.all()
    return render(request,"manager_template/employee_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def employee_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackEmployee.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def TL_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackTL.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def TL_leave_view(request):
    leaves=LeaveReportTL.objects.all()
    return render(request,"manager_template/TL_leave_view.html",{"leaves":leaves})

def employee_leave_view(request):
    leaves=LeaveReportEmployee.objects.all()
    return render(request,"manager_template/employee_leave_view.html",{"leaves":leaves})

def employee_approve_leave(request,leave_id):
    leave=LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("employee_leave_view"))

def employee_disapprove_leave(request,leave_id):
    leave=LeaveReportEmployee.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("employee_leave_view"))


def TL_approve_leave(request,leave_id):
    leave=LeaveReportTL.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("TL_leave_view"))

def TL_disapprove_leave(request,leave_id):
    leave=LeaveReportTL.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("TL_leave_view"))

def admin_view_attendance(request):
    client=Client.objects.all()
    session_year_id=SessionYearModel.object.all()
    return render(request,"manager_template/admin_view_attendance.html",{"client":client,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    client=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    client_obj=Client.objects.get(id=client)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(client_id=client_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def admin_get_attendance_employee(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for employee in attendance_data:
        data_small={"id":employee.employee_id.admin.id,"name":employee.employee_id.admin.first_name+" "+employee.employee_id.admin.last_name,"status":employee.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"manager_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def admin_send_notification_student(request):
    employee=Employee.objects.all()
    return render(request,"manager_template/employee_notification.html",{"students":employee})

def admin_send_notification_staff(request):
    tl=TL.objects.all()
    return render(request,"manager_template/TL_notification.html",{"staffs":tl})

@csrf_exempt
def send_employee_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    employee=Employee.objects.get(admin=id)
    token=employee.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Employee Management System",
            "body":message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/employee_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationEmployee(employee_id=employee,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

@csrf_exempt
def send_TL_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    tl=TL.objects.get(admin=id)
    token=tl.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Employee Management System",
            "body":message,
            "click_action":"https://studentmanagementsystem22.herokuapp.com/tl_all_notification",
            "icon":"http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationTL(TL_id=tl,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

