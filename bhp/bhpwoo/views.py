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

class ProtectiveClothesSetsReleasedView(LoginRequiredMixin, View):
    """
    This view shows a list of all protective clothing sets issued to specific employees. The release of kits can be
    done through the administration panel or from the ReleaseFormView class form (in both cases, access is limited to
    logged-in users only).
    """
    login_url = 'login'
    redirect_field_name = 'protective_clothes_sets_released'
    success_url = reverse_lazy(redirect_field_name)

    def get(self, request):
        context_object_name = 'protectiveclothessetsreleased'
        template_name = 'protectiveclothessetsreleased_list.html'
        return_data = ProtectiveClothingRelease.objects.all()
        return render(request, template_name, {context_object_name: return_data})


class ReleaseFormView(LoginRequiredMixin, FormView):
    """
    The form view is used by the site administrator to manually assign a selected set of protective clothing to a
    specific employee (access is limited to logged-in users only). This action can also be performed from the
    administration panel.
    """

    template_name = 'release_form.html'
    login_url = 'login'
    form_class = ReleaseForm
    success_url = 'protective_clothes_sets_released'

    def get(self, request):
        form = self.get_form(self.form_class)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def form_valid(self, form, *args, **kwargs):
        employee = form.cleaned_data['employee']
        pc_set = form.cleaned_data['pc_set']
        ProtectiveClothingRelease.objects.create(employee=employee, pc_set=pc_set)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(self.success_url)


class LoginView(View):
    """
    This functionality allows the user to log in
    """

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect('/')


class LogoutView(View):
    """
    This functionality allows the user to log out
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


