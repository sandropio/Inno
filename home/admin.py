from django.contrib import admin
from .models import Department, Character, MonthDay, Employee, Weekday

admin.site.register(Department)
admin.site.register(Character)
admin.site.register(MonthDay)
admin.site.register(Employee)
admin.site.register(Weekday)

