from .models import Employee, Image
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageUploadForm

def home(request):
    total_employees = Employee.objects.count()
    recent_employees = Employee.objects.order_by('-hire_date')[:4]
    return render(request, 'home.html', {
        'total_employees': total_employees,
        'recent_employees': recent_employees,
    })

def employee_list(request):
    employees = Employee.objects.all()
    paginator = Paginator(employees, 10)  # 10 сотрудников на странице
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    return render(request, 'employee_list.html', {'page_object': page_object})


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    tenure_days = (timezone.now().date() - employee.hire_date).days

    return render(request, 'employee_detail.html', {
        'employee': employee,
        'tenure_days': tenure_days,
        'first_image': employee.images.first() 
    })


def upload_image(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.employee = employee  # Привязываем изображение к сотруднику
            image.save()
            return redirect('employee_detail', employee_id=employee.id)
    else:
        form = ImageUploadForm()

    return render(request, 'upload_image.html', {'form': form, 'employee': employee})