from django.db import models
from employees.models import Employee
from django.core.exceptions import ValidationError

class Workplace(models.Model):
    desk_number = models.IntegerField(unique=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)

    def clean(self):
        if self.employee:
            adjacent_desks = [self.desk_number - 1, self.desk_number + 1]
            for desk in adjacent_desks:
                try:
                    adjacent_employee = Workplace.objects.get(desk_number=desk).employee
                    if adjacent_employee:
                        if ('tester' in adjacent_employee.skills or 'developer' in adjacent_employee.skills):
                            raise ValidationError("Тестировщики и разработчики не могут сидеть рядом!")
                except Workplace.DoesNotExist:
                    continue

    def save(self, *args, **kwargs):
        self.clean()  #Вызов очистки перед сохранением
        super().save(*args, **kwargs)