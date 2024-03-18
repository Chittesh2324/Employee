import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from module.models import Client, SessionYearModel, Employee, Attendance, AttendanceReport, \
    LeaveReportTL, TL, FeedBackTL, CustomUser, Project, NotificationTL, OnlineClassRoom


def TL_home(request):
    #For Fetch All Employee Under TL
    clients=Client.objects.filter(TL_id=request.user.id)
    project_id_list=[]
    for client in clients:
        project=Project.objects.get(id=client.project_id.id)
        project_id_list.append(project.id)

    final_project=[]
    #removing Duplicate project ID
    for project_id in project_id_list:
        if project_id not in final_project:
            final_project.append(project_id)

    employee_count=Employee.objects.filter(project_id__in=final_project).count()

    #Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(client_id__in=clients).count()

    #Fetch All Approve Leave
    tl=TL.objects.get(admin=request.user.id)
    leave_count=LeaveReportTL.objects.filter(TL_id=tl.id,leave_status=1).count()
    client_count=clients.count()

    #Fetch Attendance Data by Subject
    client_list=[]
    attendance_list=[]
    for client in clients:
        attendance_count1=Attendance.objects.filter(client_id=client.id).count()
        client_list.append(client.client_name)
        attendance_list.append(attendance_count1)

    employee_attendance=Employee.objects.filter(project_id__in=final_project)
    employee_list=[]
    employee_list_attendance_present=[]
    employee_list_attendance_absent=[]
    for employee in employee_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,employee_id=employee.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,employee_id=employee.id).count()
        employee_list.append(employee.admin.username)
        employee_list_attendance_present.append(attendance_present_count)
        employee_list_attendance_absent.append(attendance_absent_count)

    return render(request,"TL_template/TL_home_template.html",{"employee_count":employee_count,"attendance_count":attendance_count,"leave_count":leave_count,"client_count":client_count,"client_list":client_list,"attendance_list":attendance_list,"employee_list":employee_list,"present_list":employee_list_attendance_present,"absent_list":employee_list_attendance_absent})

def TL_take_attendance(request):
    client=Client.objects.filter(TL_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"TL_template/TL_take_attendance.html",{"client":client,"session_years":session_years})

@csrf_exempt
def get_employee(request):
    client_id=request.POST.get("client")
    session_year=request.POST.get("session_year")

    client=Client.objects.get(id=client_id)
    session_model=SessionYearModel.object.get(id=session_year)
    employees=Employee.objects.filter(project_id=client.project_id,session_year_id=session_model)
    list_data=[]

    for employee in employees:
        data_small={"id":employee.admin.id,"name":employee.admin.first_name+" "+employee.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    employee_ids=request.POST.get("employee_ids")
    client_id=request.POST.get("client_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    client_model=Client.objects.get(id=client_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_eemployee=json.loads(employee_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(client_id=client_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for emp in json_eemployee:
             employee=Employee.objects.get(admin=emp['id'])
             attendance_report=AttendanceReport(employee_id=employee,attendance_id=attendance,status=emp['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def TL_update_attendance(request):
    client=Client.objects.filter(TL_id=request.user.id)
    session_year_id=SessionYearModel.object.all()
    return render(request,"TL_template/TL_update_attendance.html",{"client":client,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    client=request.POST.get("client")
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
def get_attendance_employee(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for employee in attendance_data:
        data_small={"id":employee.employee_id.admin.id,"name":employee.employee_id.admin.first_name+" "+employee.employee_id.admin.last_name,"status":employee.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    employee_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_eemployee=json.loads(employee_ids)


    try:
        for emp in json_eemployee:
             employee=Employee.objects.get(admin=emp['id'])
             attendance_report=AttendanceReport.objects.get(employee_id=employee,attendance_id=attendance)
             attendance_report.status=emp['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def TL_apply_leave(request):
    tl_obj = TL.objects.get(admin=request.user.id)
    leave_data=LeaveReportTL.objects.filter(TL_id=tl_obj)
    return render(request,"TL_template/TL_apply_leave.html",{"leave_data":leave_data})

def TL_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("TL_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        tl_obj=TL.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportTL(TL_id=tl_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("TL_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("TL_apply_leave"))


def TL_feedback(request):
    tl_id=TL.objects.get(admin=request.user.id)
    feedback_data=FeedBackTL.objects.filter(TL_id=tl_id)
    return render(request,"TL_template/TL_feedback.html",{"feedback_data":feedback_data})

def TL_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("TL_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        tl_obj=TL.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackTL(TL_id=tl_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("TL_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("TL_feedback"))

def TL_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    tl=TL.objects.get(admin=user)
    return render(request,"TL_template/TL_profile.html",{"user":user,"tl":tl})

def TL_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("TL_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            tl=TL.objects.get(admin=customuser.id)
            tl.address=address
            tl.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("TL_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("TL_profile"))

@csrf_exempt
def TL_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        tl=TL.objects.get(admin=request.user.id)
        tl.fcm_token=token
        tl.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def TL_all_notification(request):
    tl=TL.objects.get(admin=request.user.id)
    notifications=NotificationTL.objects.filter(TL_id=tl.id)
    return render(request,"TL_template/all_notification.html",{"notifications":notifications})

def TL_add_result(request):
    client=Client.objects.filter(TL_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"TL_template/TL_add_result.html",{"client":client,"session_years":session_years})

'''def save_employee_result(request):
    if request.method!='POST':
        return HttpResponseRedirect('TL_add_result')
    employee_admin_id=request.POST.get('student_list')
    assignment_marks=request.POST.get('assignment_marks')
    exam_marks=request.POST.get('exam_marks')
    client_id=request.POST.get('subject')


    employee_obj=Employee.objects.get(admin=employee_admin_id)
    client_obj=Client.objects.get(id=client_id)

    try:
        check_exist=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
        if check_exist:
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_assignment_marks=assignment_marks
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("TL_add_result"))
        else:
            result=StudentResult(student_id=student_obj,subject_id=subject_obj,subject_exam_marks=exam_marks,subject_assignment_marks=assignment_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("TL_add_result"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("TL_add_result"))

@csrf_exempt
def fetch_result_employee(request):
    subject_id=request.POST.get('subject_id')
    student_id=request.POST.get('student_id')
    student_obj=Students.objects.get(admin=student_id)
    result=StudentResult.objects.filter(student_id=student_obj.id,subject_id=subject_id).exists()
    if result:
        result=StudentResult.objects.get(student_id=student_obj.id,subject_id=subject_id)
        result_data={"exam_marks":result.subject_exam_marks,"assign_marks":result.subject_assignment_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")'''

def start_live_classroom(request):
    client=Client.objects.filter(TL_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"TL_template/start_live_classroom.html",{"client":client,"session_years":session_years})

def start_live_classroom_process(request):
    session_year=request.POST.get("session_year")
    client=request.POST.get("subject")

    client_obj=Client.objects.get(id=client)
    session_obj=SessionYearModel.object.get(id=session_year)
    checks=OnlineClassRoom.objects.filter(client=client_obj,session_years=session_obj,is_active=True).exists()
    if checks:
        data=OnlineClassRoom.objects.get(client=client_obj,session_years=session_obj,is_active=True)
        room_pwd=data.room_pwd
        roomname=data.room_name
    else:
        room_pwd=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        roomname=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        tl_obj=TL.objects.get(admin=request.user.id)
        onlineClass=OnlineClassRoom(room_name=roomname,room_pwd=room_pwd,client=client_obj,session_years=session_obj,started_by=tl_obj,is_active=True)
        onlineClass.save()

    return render(request,"TL_template/live_class_room_start.html",{"username":request.user.username,"password":room_pwd,"roomid":roomname,"client":client_obj.client_name,"session_year":session_obj})


def returnHtmlWidget(request):
    return render(request,"widget.html")