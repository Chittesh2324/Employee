"""
URL configuration for Emp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from  module import views, ManagerViews, TLViews, EmployeeViews
from Emp import settings

urlpatterns = [
    path('demo',views.showDemoPage),
    path('signup_manager',views.signup_manager,name="signup_manager"),
    path('signup_employee',views.signup_employee,name="signup_employee"),
    path('signup_TL',views.signup_TL,name="signup_TL"),
    path('do_manager_signup',views.do_manager_signup,name="do_manager_signup"),
    path('do_TL_signup',views.do_TL_signup,name="do_TL_signup"),
    path('do_signup_employee',views.do_signup_employee,name="do_signup_employee"),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.ShowLoginPage,name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
    path('manager_home',ManagerViews.manager_home,name="manager_home"),
    path('add_TL',ManagerViews.add_TL,name="add_TL"),
    path('add_TL_save',ManagerViews.add_TL_save,name="add_TL_save"),
    path('add_project/', ManagerViews.add_project,name="add_project"),
    path('add_project_save', ManagerViews.add_project_save,name="add_project_save"),
    path('add_employee', ManagerViews.add_employee,name="add_employee"),
    path('add_employee_save', ManagerViews.add_employee_save,name="add_employee_save"),
    path('add_client', ManagerViews.add_client,name="add_client"),
    path('add_client_save', ManagerViews.add_client_save,name="add_client_save"),
    path('manage_TL', ManagerViews.manage_TL,name="manage_TL"),
    path('manage_employee', ManagerViews.manage_employee,name="manage_employee"),
    path('manage_project', ManagerViews.manage_project,name="manage_project"),
    path('manage_client', ManagerViews.manage_client,name="manage_client"),
    path('edit_TL/<str:TL_id>', ManagerViews.edit_TL,name="edit_TL"),
    path('edit_TL_save', ManagerViews.edit_TL_save,name="edit_TL_save"),
    path('edit_employee/<str:employee_id>', ManagerViews.edit_employee,name="edit_employee"),
    path('edit_employee_save', ManagerViews.edit_employee_save,name="edit_employee_save"),
    path('edit_client/<str:client_id>', ManagerViews.edit_client,name="edit_client"),
    path('edit_client_save', ManagerViews.edit_client_save,name="edit_client_save"),
    path('edit_project/<str:project_id>', ManagerViews.edit_project,name="edit_project"),
    path('edit_project_save', ManagerViews.edit_project_save,name="edit_project_save"),
    path('manage_session', ManagerViews.manage_session,name="manage_session"),
    path('add_session_save', ManagerViews.add_session_save,name="add_session_save"),
    path('check_email_exist', ManagerViews.check_email_exist,name="check_email_exist"),
    path('check_username_exist', ManagerViews.check_username_exist,name="check_username_exist"),
    path('employee_feedback_message', ManagerViews.employee_feedback_message,name="employee_feedback_message"),
    path('employee_feedback_message_replied', ManagerViews.employee_feedback_message_replied,name="employee_feedback_message_replied"),
    path('TL_feedback_message', ManagerViews.TL_feedback_message,name="TL_feedback_message"),
    path('TL_feedback_message_replied', ManagerViews.TL_feedback_message_replied,name="TL_feedback_message_replied"),
    path('employee_leave_view', ManagerViews.employee_leave_view,name="employee_leave_view"),
    path('TL_leave_view', ManagerViews.TL_leave_view,name="TL_leave_view"),
    path('employee_approve_leave/<str:leave_id>', ManagerViews.employee_approve_leave,name="employee_approve_leave"),
    path('employee_disapprove_leave/<str:leave_id>', ManagerViews.employee_disapprove_leave,name="employee_disapprove_leave"),
    path('TL_disapprove_leave/<str:leave_id>', ManagerViews.TL_disapprove_leave,name="TL_disapprove_leave"),
    path('TL_approve_leave/<str:leave_id>', ManagerViews.TL_approve_leave,name="TL_approve_leave"),
    path('admin_view_attendance', ManagerViews.admin_view_attendance,name="admin_view_attendance"),
    path('admin_get_attendance_dates', ManagerViews.admin_get_attendance_dates,name="admin_get_attendance_dates"),
    path('admin_get_attendance_employee', ManagerViews.admin_get_attendance_employee,name="admin_get_attendance_employee"),
    path('admin_profile', ManagerViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', ManagerViews.admin_profile_save,name="admin_profile_save"),
    path('admin_send_notification_staff', ManagerViews.admin_send_notification_staff,name="admin_send_notification_staff"),
    path('admin_send_notification_student', ManagerViews.admin_send_notification_student,name="admin_send_notification_student"),
    path('send_employee_notification', ManagerViews.send_employee_notification,name="send_employee_notification"),
    path('send_TL_notification', ManagerViews.send_TL_notification,name="send_TL_notification"),

                  #     Staff URL Path
    path('TL_home', TLViews.TL_home, name="TL_home"),
    path('TL_take_attendance', TLViews.TL_take_attendance, name="TL_take_attendance"),
    path('TL_update_attendance', TLViews.TL_update_attendance, name="TL_update_attendance"),
    path('get_employee', TLViews.get_employee, name="get_employee"),
    path('get_attendance_dates', TLViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_employee', TLViews.get_attendance_employee, name="get_attendance_employee"),
    path('save_attendance_data', TLViews.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data', TLViews.save_updateattendance_data, name="save_updateattendance_data"),
    path('TL_apply_leave', TLViews.TL_apply_leave, name="TL_apply_leave"),
    path('TL_apply_leave_save', TLViews.TL_apply_leave_save, name="TL_apply_leave_save"),
    path('TL_feedback', TLViews.TL_feedback, name="TL_feedback"),
    path('TL_feedback_save', TLViews.TL_feedback_save, name="TL_feedback_save"),
    path('TL_profile', TLViews.TL_profile, name="TL_profile"),
    path('TL_profile_save', TLViews.TL_profile_save, name="TL_profile_save"),
    path('TL_fcmtoken_save', TLViews.TL_fcmtoken_save, name="TL_fcmtoken_save"),
    path('TL_all_notification', TLViews.TL_all_notification, name="TL_all_notification"),
    path('TL_add_result', TLViews.TL_add_result, name="TL_add_result"),
    #path('save_employee_result', TLViews.save_employee_result, name="save_employee_result"),
    #path('edit_student_result',EditResultViewClass.as_view(), name="edit_student_result"),
   # path('fetch_result_employee',TLViews.fetch_result_employee, name="fetch_result_employee"),
    path('start_live_classroom',TLViews.start_live_classroom, name="start_live_classroom"),
    path('start_live_classroom_process',TLViews.start_live_classroom_process, name="start_live_classroom_process"),


    path('employee_home', EmployeeViews.employee_home, name="employee_home"),
    path('employee_view_attendance', EmployeeViews.employee_view_attendance, name="employee_view_attendance"),
    path('employee_view_attendance_post', EmployeeViews.employee_view_attendance_post, name="employee_view_attendance_post"),
    path('employee_apply_leave', EmployeeViews.employee_apply_leave, name="employee_apply_leave"),
    path('employee_apply_leave_save', EmployeeViews.employee_apply_leave_save, name="employee_apply_leave_save"),
    path('employee_feedback', EmployeeViews.employee_feedback, name="employee_feedback"),
    path('employee_feedback_save', EmployeeViews.employee_feedback_save, name="employee_feedback_save"),
    path('employee_profile', EmployeeViews.employee_profile, name="employee_profile"),
    path('employee_profile_save', EmployeeViews.employee_profile_save, name="employee_profile_save"),
    path('employee_fcmtoken_save', EmployeeViews.employee_fcmtoken_save, name="employee_fcmtoken_save"),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    path('employee_all_notification',EmployeeViews.employee_all_notification,name="employee_all_notification"),
    #path('employee_view_result',EmployeeViews.employee_view_result,name="employee_view_result"),
    path('join_class_room/<int:subject_id>/<int:session_year_id>',EmployeeViews.join_class_room,name="join_class_room"),
    path('node_modules/canvas-designer/widget.html',TLViews.returnHtmlWidget,name="returnHtmlWidget"),
    path('testurl/',views.Testurl)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

