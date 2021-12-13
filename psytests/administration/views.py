from django.contrib.auth import models
from django.contrib.auth.models import User
from django.forms import fields
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, CreateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import SearchForm
from accounts.models import Profile
from accounts.forms import UpdateUserForm


# Create your views here.
class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

class Home(LoginRequiredMixin, SuperUserCheck ,TemplateView):
    template_name = 'administration/admin_home.html'

class UserManagement(LoginRequiredMixin, SuperUserCheck ,ListView):
    template_name = 'administration/user_management.html'
    model = User
    context_object_name = 'users'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('name')
        if query:
            object_list = self.model.objects.filter(username__icontains=query).exclude(username=self.request.user)
        else:
            object_list = self.model.objects.exclude(username=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm
        context['users_total'] = self.get_queryset().count()
        context['unapproved_users'] = Profile.objects.filter(is_approved=False).count()

        return context

class UserDetailUpdate(LoginRequiredMixin, SuperUserCheck , UpdateView):
    template_name = 'administration/user_detail_update.html'
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('administration:user-management')

class UnapprovedUsers(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = 'administration/unapproved_users.html'
    model = Profile
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('name')
        if query:
            object_list = self.model.objects.filter(user__username__icontains=query, is_approved__isnull=False).order_by('is_approved')
        else:
            object_list = self.model.objects.exclude(is_approved=None).order_by('is_approved')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm
        context['users_total'] = self.get_queryset().count()
        context['unapproved_users'] = Profile.objects.filter(is_approved=False).count()

        return context

def approve_user(request):
    get_pk = request.POST['value']
    obj = Profile.objects.get(id=get_pk)
    if obj.is_approved == True:
        obj.is_approved = False
    else:
        obj.is_approved = True
    obj.save()

    return redirect('administration:unapproved-users')