from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import ImageForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json  # Import json
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import AllowAny
from .serializers import EmployeeSerializer, EmployeeDetailSerializer
from rest_framework.decorators import permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EmployeeFilter



def home(request):
    context = {
        'page_title': 'Главная страница',
        'welcome_message': 'Добро пожаловать!',
    }
    return render(request, 'home.html', context)

def employee_list(request):
    employees = Employee.objects.order_by('username')
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
            try:
                image = form.save(commit=False)
                image.employee = employee
                image.save()
                messages.success(request, 'Изображение успешно загружено!')
                return redirect('employee_detail', employee_id=employee_id)
            except Exception as e:
                messages.error(request, f'Произошла ошибка при загрузке изображения: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ImageForm()

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'upload_image.html', context)

class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ['skills']
    ordering_fields = ['hire_date', 'experience']

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer
    permission_classes = [IsAuthenticated]



class IsVisitor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Посетитель').exists()

class IsOverseer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Смотритель').exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Администратор').exists()

class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsVisitor()|IsOverseer()|IsAdmin()]
        else:
            return [IsAuthenticated(), IsAdmin()]

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsVisitor()|IsOverseer()|IsAdmin()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsOverseer()|IsAdmin()]
        else:
            return [IsAuthenticated(), IsAdmin()]
