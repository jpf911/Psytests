from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, CreateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.
class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

class Home(LoginRequiredMixin,SuperUserCheck,TemplateView):
    template_name = 'administration/admin_home.html'