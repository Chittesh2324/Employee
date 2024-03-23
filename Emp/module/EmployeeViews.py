import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from module.models import Employee, Project, Client, CustomUser, Attendance, AttendanceReport, \
    LeaveReportEmployee, FeedBackEmployee, NotificationEmployee, OnlineClassRoom, SessionYearModel


def employee_home(request):
    employee_obj=Employee.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(employee_id=employee_obj).count()
    attendance_present=AttendanceReport.objects.filter(employee_id=employee_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(employee_id=employee_obj,status=False).count()
    project=Project.objects.get(id=employee_obj.project_id.id)
    client=Client.objects.filter(project_id=project).count()
    client_data=Client.objects.filter(project_id=project)
    session_obj=SessionYearModel.object.get(id=employee_obj.session_year_id.id)
    class_room=OnlineClassRoom.objects.filter(client__in=client_data,is_active=True,session_years=session_obj)

    client_name=[]
    data_present=[]
    data_absent=[]
    client_data=Client.objects.filter(project_id=employee_obj.project_id)
    for clients in client_data:
        attendance=Attendance.objects.filter(client_id=clients.id)
        attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,employee_id=employee_obj.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,employee_id=employee_obj.id).count()
        client_name.append(clients.client_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request,"employee_template/employee_home_template.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"client":client,"data_name":client_name,"data1":data_present,"data2":data_absent,"class_room":class_room})

def join_class_room(request,client_id,session_year_id):
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    client=Client.objects.filter(id=client_id)
    if client.exists():
        session=SessionYearModel.object.filter(id=session_year_obj.id)
        if session.exists():
            client_obj=Client.objects.get(id=client_id)
            project=Project.objects.get(id=client_obj.project_id.id)
            check_project=Employee.objects.filter(admin=request.user.id,project_id=project.id)
            if check_project.exists():
                session_check=Employee.objects.filter(admin=request.user.id,session_year_id=session_year_obj.id)
                if session_check.exists():
                    onlineclass=OnlineClassRoom.objects.get(session_years=session_year_id,client=client_id)
                    return render(request,"employee_template/join_class_room_start.html",{"username":request.user.username,"password":onlineclass.room_pwd,"roomid":onlineclass.room_name})

                else:
                    return HttpResponse("This Online Session is Not For You")
            else:
                return HttpResponse("This Subject is Not For You")
        else:
            return HttpResponse("Session Year Not Found")
    else:
        return HttpResponse("Subject Not Found")


def employee_view_attendance(request):
    employee=Employee.objects.get(admin=request.user.id)
    project=employee.project_id
    client=Client.objects.filter(project_id=project)
    return render(request,"employee_template/employee_view_attendance.html",{"client":client})

def employee_view_attendance_post(request):
    client_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    client_obj=Client.objects.get(id=client_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    emp_obj=Employee.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),client_id=client_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,employee_id=emp_obj)
    return render(request,"employee_template/employee_attendance_data.html",{"attendance_reports":attendance_reports})

def employee_apply_leave(request):
    tl_obj = Employee.objects.get(admin=request.user.id)
    leave_data=LeaveReportEmployee.objects.filter(employee_id=tl_obj)
    return render(request,"employee_template/employee_apply_leave.html",{"leave_data":leave_data})

def employee_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("employee_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        employee_obj=Employee.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportEmployee(employee_id=employee_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("employee_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("employee_apply_leave"))


def employee_feedback(request):
    tl_id=Employee.objects.get(admin=request.user.id)
    feedback_data=FeedBackEmployee.objects.filter(employee_id=tl_id)
    return render(request,"employee_template/employee_feedback.html",{"feedback_data":feedback_data})

def employee_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("employee_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        employee_obj=Employee.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackEmployee(employee_id=employee_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("employee_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("employee_feedback"))

def employee_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    employee=Employee.objects.get(admin=user)
    return render(request,"employee_template/employee_profile.html",{"user":user,"employee":employee})

def employee_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("employee_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            employee=Employee.objects.get(admin=customuser)
            employee.address=address
            employee.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("employee_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("employee_profile"))

@csrf_exempt
def employee_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        employee=Employee.objects.get(admin=request.user.id)
        employee.fcm_token=token
        employee.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def employee_all_notification(request):
    employee=Employee.objects.get(admin=request.user.id)
    notifications=NotificationEmployee.objects.filter(employee_id=employee.id)
    return render(request,"employee_template/all_notification.html",{"notifications":notifications})

'''def employee_view_result(request):
    employee=Employee.objects.get(admin=request.user.id)
    studentresult=StudentResult.objects.filter(student_id=student.id)
    return render(request,"employee_template/employee_result.html",{"studentresult":studentresult})'''