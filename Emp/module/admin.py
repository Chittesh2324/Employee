from django.contrib import admin
from module.models import CustomUser,SessionYearModel,AdminManager,TL,Project, \
    Client,Employee,Attendance,AttendanceReport,LeaveReportEmployee,LeaveReportTL,\
    FeedBackEmployee,FeedBackTL,NotificationEmployee,NotificationTL
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(SessionYearModel)
admin.site.register(AdminManager)
admin.site.register(TL)
admin.site.register(Project)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportEmployee)
admin.site.register(LeaveReportTL)
admin.site.register(FeedBackEmployee)
admin.site.register(FeedBackTL)
admin.site.register(NotificationEmployee)
admin.site.register(NotificationTL)
