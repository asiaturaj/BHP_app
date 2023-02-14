from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ReleaseForm
from .models import Employee, ProtectiveClothing, ProtectiveClothingSet, ProtectiveClothingRelease


class EmployeeView(View):
    """
    This view is responsible for displaying basic information about the employee.
    """

    def get(self, request):
        context_object_name = 'employees'
        template_name = 'employee_list.html'
        return_data = Employee.objects.all()
        return render(request, template_name, {context_object_name: return_data})


class EmployeeDetailView(View):
    """
    This view is responsible for displaying detailed information about the employee.
    """

    def get(self, request, employee_id):
        context_object_name = 'employee'
        template_name = 'employee_detail.html'
        return_data = Employee.objects.get(id=employee_id)
        return render(request, template_name, {context_object_name: return_data})


class ProtectiveClothesView(View):
    """
    This view is responsible for displaying a list of available protective clothing items
    """

    def get(self, request):
        context_object_name = 'protectiveclothes'
        template_name = 'protectiveclothes_list.html'
        return_data = ProtectiveClothing.objects.all()
        return render(request, template_name, {context_object_name: return_data})


class ProtectiveClothesSetsView(View):
    """
    This view is used to show information about protective clothing sets. Each kit is adapted for workers in a
    specific position.
    """

    def get(self, request):
        context_object_name = 'protectiveclothessets'
        template_name = 'protectiveclothesset_list.html'
        return_data = ProtectiveClothingSet.objects.all()
        return render(request, template_name, {context_object_name: return_data})


class ProtectiveClothesSetDetailView(View):
    """
    This view provides detailed information about the selected specific set of protective clothing. In addition to
    basic information, you will find the price of the entire set and the number of protective clothing items that
    comprise it.
    """

    def get(self, request, set_id):
        context_object_name = 'protectiveclothingset'
        template_name = 'protectiveclothesset_detail.html'
        return_data = ProtectiveClothingSet.objects.get(id=set_id)
        return render(request, template_name, {context_object_name: return_data})


