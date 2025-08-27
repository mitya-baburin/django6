from django.test import TestCase
import json
from .models import Employee, Desk
from django.core.exceptions import ValidationError
from django.urls import reverse

class EmployeeFormTest(TestCase):

    def test_employee_form_valid(self):
        """Тестирование валидной формы со всеми данными."""
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'gender': 'M',
            'skills': [],  # Передаем пустой список
            'hire_date': '2024-01-01',
        }
        employee = Employee.objects.create(**form_data)
        self.assertEqual(employee.skills, [])

    def test_employee_form_valid_missing_optional_data(self):
        """Тестирование валидной формы с пропущенными необязательными данными."""
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        employee = Employee.objects.create(**form_data)
        self.assertEqual(employee.username, form_data['username'])
        self.assertEqual(employee.password, form_data['password'])

class HomePageContextTest(TestCase):
    def test_home_page_context(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('page_title', response.context)
        self.assertEqual(response.context['page_title'], 'Главная страница')
        self.assertIn('welcome_message', response.context)
        self.assertEqual(response.context['welcome_message'], 'Добро пожаловать!')

class EmployeeListContextTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            username='testuser',
            password='testpassword',
            gender='M',
            skills=[],
            hire_date='2024-01-01'
        )

    def test_employee_list_page_context(self):
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_list.html')
        self.assertIn('employee_list', response.context)
        self.assertTrue(response.context['employee_list'].object_list)
        self.assertIn(self.employee, response.context['employee_list'])

class DeskArrangementValidatorTest(TestCase):

    def setUp(self):
        self.desk1 = Desk.objects.create(number=1)
        self.desk2 = Desk.objects.create(number=2)
        self.desk3 = Desk.objects.create(number=3)

        self.developer1 = Employee.objects.create_user(username='developer1', password='testpassword', role='developer', desk=self.desk1)
        self.developer2 = Employee.objects.create_user(username='developer2', password='testpassword', role='developer', desk=self.desk2)
        self.tester1 = Employee.objects.create_user(username='tester1', password='testpassword', role='tester', desk=self.desk3)
        self.manager1 = Employee.objects.create_user(username='manager1', password='testpassword')

    def test_developer_and_tester_cannot_sit_next_to_each_other(self):
        self.tester1.desk = self.desk1
        with self.assertRaises(ValidationError):
            self.tester1.full_clean()
            self.tester1.save()

    def test_developers_can_sit_next_to_each_other(self):
        try:
            self.developer2.desk = self.desk1
            self.developer2.full_clean()
            self.developer2.save()
        except ValidationError:
            self.fail("Разработчики могут сидеть рядом.")

    def test_other_roles_can_sit_next_to_developers_or_testers(self):
        try:
            self.manager1.desk = self.desk1
            self.manager1.save()
        except ValidationError:
            self.fail("Сотрудники с другими ролями могут сидеть рядом с разработчиками и тестировщиками.")