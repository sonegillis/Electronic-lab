from django.contrib import admin
from .models import WeekDaySchedule, Staff, Students, StaffBookings, StudentBookings, BookedDates
# Register your models here.
admin.site.register(WeekDaySchedule)
admin.site.register(Staff)
admin.site.register(Students)
admin.site.register(StaffBookings)
admin.site.register(StudentBookings)
admin.site.register(BookedDates)
