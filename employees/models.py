from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Employee(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    skills = models.JSONField() 
    hire_date = models.DateField()

    # Переопределяем поля для групп и разрешений
    groups = models.ManyToManyField(
        Group,
        related_name="employees",  # Переопределите имя обратной связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="employees",  # Переопределите имя обратной связи
        blank=True
    )

class Image(models.Model):
    employee = models.ForeignKey(Employee, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='employee_images/')
    order = models.PositiveIntegerField(default=0)

    def delete(self, *args, **kwargs):
        self.image.delete()  
        super().delete(*args, **kwargs)
  