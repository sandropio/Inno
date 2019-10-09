from django.db import models
import json


class Character(models.Model):
    char = models.CharField(max_length=30)

    def __str__(self):
        return self.char


class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Employee(models.Model):
    fist_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='employee_images')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    characters = models.ManyToManyField(Character)

    def __str__(self):
        return self.fist_name + ' ' + self.last_name


class Weekday(models.Model):
    day = models.CharField(max_length=50)

    def __str__(self):
        return self.day


class MonthDay(models.Model):
    days = models.ManyToManyField(Weekday)
    start = models.TimeField(auto_now=False, auto_now_add=False)
    end = models.TimeField(auto_now=False, auto_now_add=False)
    connect = models.ForeignKey(Employee, on_delete=models.CASCADE)


class CalendarEventObject(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_date_time = models.DateTimeField(blank=True, null=True)
    event_end_date_time = models.DateTimeField(blank=True, null=True)
    event_name = models.CharField(max_length=256, blank=True, null=True, default="Innotec Event")


