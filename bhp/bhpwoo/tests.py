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

   