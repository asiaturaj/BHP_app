from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Employee, Position

import pytest


class PageTest(TestCase):
    """
    This class have tests that mostly check if page opens correctly, use proper template, contains text or is available by name
    """

    def setUp(self):
        """
        Setup that creates objects for test database
        """
        position = Position.objects.create(position_type="ET")
        self.obj1 = Employee.objects.create(first_name="Bolesław", last_name="Baczuk", sex="M", age=75,
                                            position=position)
        self.obj2 = Employee.objects.create(first_name="Andrzej", last_name="Banicki", sex="M", age=44,
                                            position=position)
        position2 = Position.objects.create(position_type="EL")
        self.obj3 = Employee.objects.create(first_name="Marek", last_name="Jagodziński", sex="M", age=33,
                                            position=position2)
        self.obj4 = Employee.objects.create(first_name="Krzysztof", last_name="Baniuk", sex="M", age=29,
                                            position=position2)

    def test_home_page(self):
        """
        Tests if home page is opening and checks if status code is OK (200)
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_content(self):
        """
        This test checks if response contains particular texts
        """
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Wszyscy pracownicy:")
        self.assertContains(response, "Odzież ochronna")
        self.assertContains(response, "Zaloguj się...")
        self.assertNotContains(response, "Wydane zestawy")
        self.assertNotContains(response, "Wydaj zestaw")

    def test_home_page_url_available_by_name(self):
        """
        Checks if home page is available by name
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_name_correct(self):
        """
        Tests if home page use proper template
        """
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "employee_list.html")

    def test_pc_page(self):
        """
        Tests if protective clothes page is opening and checks if status code is OK (200)
        """
        response = self.client.get('/protective-clothes/')
        self.assertEqual(response.status_code, 200)

    def test_pc_page_url_available_by_name(self):
        """
        Checks if protective clothes page is available by name
        """
        response = self.client.get(reverse("protective_clothes"))
        self.assertEqual(response.status_code, 200)

    def test_pc_page_template_name_correct(self):
        """
        Tests if protective clothes page use proper template
        """
        response = self.client.get(reverse("protective_clothes"))
        self.assertTemplateUsed(response, "protectiveclothes_list.html")

    def test_pc_page_template_content(self):
        """
        This test checks if response contains particular text
        """
        response = self.client.get(reverse("protective_clothes"))
        self.assertContains(response, "Odzież ochronna:")

    def test_pcs_page(self):
        """
        Tests if protective clothes sets page is opening and checks if status code is OK (200)
        """
        response = self.client.get('/protective-clothes-sets/')
        self.assertEqual(response.status_code, 200)

    def test_pcs_page_url_available_by_name(self):
        """
        Checks if protective clothes sets page is available by name
        """
        response = self.client.get(reverse("protective_clothes_sets"))
        self.assertEqual(response.status_code, 200)

    def test_pcs_page_template_name_correct(self):
        """
        Tests if protective clothes sets page use proper template
        """
        response = self.client.get(reverse("protective_clothes_sets"))
        self.assertTemplateUsed(response, "protectiveclothesset_list.html")

    def test_pcs_page_template_content(self):
        """
        This test checks if response contains particular text
        """
        response = self.client.get(reverse("protective_clothes_sets"))
        self.assertContains(response, "Wszystkie zestawy BHP:")

    def test_admin_page(self):
        """
        Tests if admin page is opening and checks if it redirects to login page, code is (302)
        """
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/admin/login/?next=/admin/', status_code=302)

    def test_login_form_page(self):
        """
        Tests if login form page is opening and checks if status code is OK (200)
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_form_url_available_by_name(self):
        """
        Checks if login form page is available by name
        """
        response = self.client.get(reverse("form"))
        self.assertEqual(response.status_code, 302)

    def test_logout_page(self):
        """
        Tests if logout page is opening and checks if status code is OK (200)
        """
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/', status_code=302)

    def test_employee_detail_page_available_by_name(self):
        """
        Check if detail page for Employee opens for two created objects
        """
        url = reverse('employee_detail', args=[self.obj2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        url = reverse('employee_detail', args=[self.obj3.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_employee_detail_page_template_name_correct(self):
        """
        Check if detail page for Employee use proper template
        """
        url = reverse('employee_detail', args=[self.obj1.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "employee_detail.html")

    def test_employee_detail_page_template_content(self):
        """
        Check if detail page for Employee contains particular texts
        """
        url = reverse('employee_detail', args=[self.obj1.id])
        response = self.client.get(url)
        self.assertContains(response, "Szczegółowe informacje o pracowniku:")
        self.assertContains(response, "Bolesław")
        self.assertContains(response, "Baczuk")


class EmployeeModelTest(TestCase):
    """
    This test class allow to check if creating new Employee objects works correct
    """

    @classmethod
    def setUpTestData(cls):
        """
        Setup method ads new employee and position objects for further tests
        """
        position = Position.objects.create(position_type="ET")
        cls.employee = Employee.objects.create(first_name="Adam", last_name="Kaziuk", sex="M", age=45,
                                               position=position)

    def test_model_content(self):
        """
        Test method checks if particular fields have proper values
        """
        self.assertEqual(self.employee.first_name, "Adam")
        self.assertEqual(self.employee.last_name, "Kaziuk")
        self.assertEqual(self.employee.sex, "M")
        self.assertEqual(self.employee.age, 45)

    def test_url_exists_at_correct_location(self):
        """
        Test method checks if location '/' is correct and page opens properly
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        """
        Test method checks if location 'home' is correct, page opens properly and contains used before text values
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employee_list.html")
        self.assertContains(response, "Adam")
        self.assertContains(response, "Kaziuk")


class LogInTest(TestCase):
    """
    This test checks login (with good credentials), logout, and again login (but with wrong credentials)
    """

    def setUp(self):
        self.credentials = {
            'username': 'admin2',
            'password': 'pass2'}

        User.objects.create_user(**self.credentials)

        self.wrong_credentials = {
            'username': 'admin23543sdfasdfds',
            'password': 'pass534543dfsdfgsdf'}

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        response_logout = self.client.get('/logout/', follow=True)
        response2 = self.client.post('/login/', self.wrong_credentials, follow=True)
        self.assertFalse(response2.context['user'].is_active)


@pytest.fixture
def create_user(db, django_user_model):
    """
    Create user fixture for further tests
    """

    def make_user(**kwargs):
        kwargs['username'] = 'admin2'
        kwargs['password'] = 'pass2'
        return django_user_model.objects.create(**kwargs)

    return make_user


@pytest.mark.django_db
def test_employee_create(create_user):
    """
    Tests if model is created properly by checking number of employees
    """
    position = Position.objects.create(position_type="ET")
    Employee.objects.create(first_name="Bolesław", last_name="Baczuk", sex="M", age=75, position=position)
    Employee.objects.create(first_name="Andrzej", last_name="Bania", sex="M", age=75, position=position)
    Employee.objects.create(first_name="Wojtek", last_name="Kacen", sex="M", age=75, position=position)
    assert Employee.objects.count() == 3


@pytest.mark.django_db
def test_employee_view(client):
    """
    Checks Employee list view
    """
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_pcs_view(client):
    """
    Checks protection clothes sets view
    """
    url = reverse('protective_clothes_sets')
    response = client.get(url)
    assert response.status_code == 200
