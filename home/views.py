from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Employee, Character, Department, MonthDay, CalendarEventObject
import datetime
import hashlib

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def calendar_view(request, employee_id):
    calendar_employee = MonthDay.objects.filter(connect_id=employee_id).first()
    ctx = {}
    ctx['calendar'] = calendar_employee
    ctx['employee_id'] = employee_id
    return render(request, 'calendar.html', ctx)


def get_calendar_data(request, employee_id):
    calendar_employee = CalendarEventObject.objects.filter(employee__id=employee_id)
    data = [{"id": x.id, "title": x.event_name, "start": x.event_date_time, "end": x.event_end_date_time} for x in
            calendar_employee]
    return JsonResponse(data=data, status=200, safe=False)


def set_employee_event(request, employee_id):
    data = request.POST

    event_start_date = None
    event_end_date = None

    if data.get('event_start_str'):
        event_start_date = datetime.datetime.strptime(data.get('event_start_str'), "%Y-%m-%d")

    if data.get("event_end_str"):
        event_end_date = datetime.datetime.strptime(data.get("event_end_str"), "%Y-%m-%d")

    start_time = data.get("event-start")
    end_time = data.get("event-end")
    sh, sm = start_time.split(":")
    eh, em = None, None

    if end_time:
        eh, em = end_time.split(":")

    for date in daterange(event_start_date, event_end_date):
        date_start = date
        date_end = date

        date_start = date_start.replace(hour=int(sh), minute=int(sm))

        if end_time:
            date_end = date_end.replace(hour=int(eh), minute=int(em))

        CalendarEventObject.objects.create(
            employee_id=employee_id,
            event_date_time=date_start,
            event_end_date_time=date_end,
            event_name=data.get("event-name")
        )
    return HttpResponseRedirect(reverse("calendar", kwargs={"employee_id": employee_id}))


@csrf_exempt
def update_event(request):
    data = request.POST
    event = CalendarEventObject.objects.get(id=data.get("id"))

    if data.get("newtime"):
        new_time = datetime.datetime.strptime(data.get("newtime")[:16], "%Y-%m-%dT%H:%M")
        event.event_end_date_time = new_time

    if data.get("newtimestart"):
        new_time_start = datetime.datetime.strptime(data.get("newtimestart")[:16], "%Y-%m-%dT%H:%M")
        event.event_date_time = new_time_start

    event.save()
    return JsonResponse(data={"status": "ok"}, status=200)


def index(request):
    departments = Department.objects.all()
    characters = Character.objects.all()

    ctx = {}
    ctx['departments'] = departments
    ctx['characters'] = characters
    return render(request, 'index.html', ctx)


def department(request):
    employees = Employee.objects.all()
    departments = Department.objects.all()
    dep_id = request.GET.get("department")
    dep_id = dep_id if dep_id != '-1' else None

    if dep_id:
        dep = Department.objects.get(id=dep_id)
        employees = dep.employee_set.all()

    ctx = {}
    ctx['dep_id'] = dep_id
    ctx['departments'] = departments
    ctx['employees'] = employees
    return render(request, 'departamenti.html', ctx)


def employees(request):
    employees_list = Employee.objects.all()
    departments = Department.objects.all()

    ctx = {}
    ctx['employees'] = employees_list
    ctx['departments'] = departments
    return render(request, 'employes.html', ctx)


def delete_employees(request, employee_id):
    employee = Employee.objects.filter(id=employee_id).first()
    if employee:
        employee.delete()
    return HttpResponseRedirect('/employees')


def delete_employee(request, employee_id):
    employee = Employee.objects.filter(id=employee_id).first()
    if employee:
        employee.delete()
    return HttpResponseRedirect('/department')


def management(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        username = request.POST.get('username')
        password = request.POST.get('password')
        picutre = request.FILES.get('picture')
        department = request.POST.get('department')
        department = department if department != '-1' else None
        charact = request.POST.getlist('character')
        charact = charact if charact != '-1' else []

        emp = Employee.objects.create(
            fist_name=first_name,
            last_name=last_name,
            username=username,
            password=hashlib.sha256(password.encode()).hexdigest(),
            email=email,
            mobile=mobile,
            picture=picutre,
            department_id=department,
        )
        if charact:
            char = Character.objects.filter(id__in=charact)
            for ch in char:
                emp.characters.add(ch)

        ctx = {'message': 'Employee Added Successfully'}
        character_list = Character.objects.all()
        departments = Department.objects.all()
        ctx['characters'] = character_list
        ctx['departments'] = departments
        return render(request, 'index.html', context=ctx)
