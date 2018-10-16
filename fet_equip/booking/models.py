from django.db import models

weekDays = (
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
)

weekDaysDict = {
    0 : "Monday",
    1 : "Tuesday",
    2 : "Wednesday",
    3 : "Thursday",
    4 : "Friday",
    5 : "Saturday",
    6 : "Sunday",
}

staffBookingReason = (
    ("WORK", "work"),
    ("CLASS", "class"),
)

# Create your models here.

class WeekDaySchedule(models.Model):
    weekDay = models.IntegerField(choices = weekDays)
    fromTime = models.TimeField()
    toTime = models.TimeField()
    maxBookings = models.IntegerField(default=10)
    maxBookingsReached = models.BooleanField(default=False)

    def __str__(self):
        return weekDaysDict[self.weekDay] + ", From " + str(self.fromTime) + " - " + str(self.toTime) + " Max - " + str(self.maxBookings) 

class Staff(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.firstName + " " + self.lastName + " >>>> " + self.phoneNumber

class Students(models.Model):
    matricule = models.CharField(max_length=15, unique=True)
    phoneNumber = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.matricule + " ------ " + self.phoneNumber

class StudentBookings(models.Model):
    period = models.ForeignKey(WeekDaySchedule, on_delete=models.CASCADE)
    student = models.ForeignKey(Students)

class StaffBookings(models.Model):
    period = models.ForeignKey(WeekDaySchedule, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff)
    reason = models.CharField(max_length=8, choices=staffBookingReason)

class BookedDates(models.Model):
    period = models.ForeignKey(WeekDaySchedule)
    date = models.DateField()
    numberOfBookings = models.IntegerField()


