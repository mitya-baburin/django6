import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    skills = django_filters.CharFilter(field_name='skills', lookup_expr='icontains')
    experience = django_filters.NumberFilter(field_name='experience')  # Предполагается, что у вас есть поле experience в модели Employee
    experience__gt = django_filters.NumberFilter(field_name='experience', lookup_expr='gt')
    experience__lt = django_filters.NumberFilter(field_name='experience', lookup_expr='lt')

    class Meta:
        model = Employee
        fields = ['skills', 'experience', 'experience__gt', 'experience__lt']