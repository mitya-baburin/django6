from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

class Desk(models.Model):
    number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Стол №{self.number}"

class Employee(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    skills = models.JSONField(
        blank=True,
        null=True
    )
    hire_date = models.DateField(
        blank=True,
        null=True
    )
    role = models.CharField(max_length=50, default='employee')
    desk = models.ForeignKey(Desk, on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="employees",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="employees",
        blank=True
    )

    def clean(self):
        if self.desk:
            employees_at_desk = Employee.objects.filter(desk=self.desk).exclude(pk=self.pk)
            for employee in employees_at_desk:
                if (self.role == 'developer' and employee.role == 'tester') or \
                   (self.role == 'tester' and employee.role == 'developer'):
                    raise ValidationError("Разработчик и тестировщик не могут сидеть за одним столом!")

    def save(self, *args, **kwargs):
        self.full_clean()  #full_clean() перед сохранением
        super().save(*args, **kwargs)

class Image(models.Model):
    employee = models.ForeignKey(Employee, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='employee_images/')
    order = models.PositiveIntegerField(default=0)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)