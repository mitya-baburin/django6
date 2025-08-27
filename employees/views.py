# employees/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm, ImageUploadForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageForm

def home(request):
    context = {
        'page_title': 'Главная страница',
        'welcome_message': 'Добро пожаловать!',
    }
    return render(request, 'home.html', context)

def employee_list(request):
    employees = Employee.objects.order_by('username')  # Упорядочиваем список
    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    context = {
        'employee_list': employees,
    }
    return render(request, 'employee_list.html', context)

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    context = {
        'employee': employee,
    }
    return render(request, 'employee_detail.html', context)

def upload_image(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.employee = employee
            image.save()
            # Перенаправление или отображение сообщения об успехе
    else:
        form = ImageForm()
    return render(request, 'employees/upload_image.html', {'form': form, 'employee': employee})
   
    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'upload_image.html', context)