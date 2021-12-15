from django.contrib.auth import models
from django.contrib.auth.models import User
from django.forms import fields
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

from psytests.views import NotifCount

from datetime import datetime

from .forms import ScheduleDateForm, SearchForm
from .models import AdminScheduledConsultation

from accounts.models import Profile
from accounts.forms import UpdateUserForm

now = datetime.today()

# Create your views here.
class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser


class Home(LoginRequiredMixin, SuperUserCheck, NotifCount, TemplateView):
    template_name = "administration/admin_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        return context


class UserManagement(LoginRequiredMixin, SuperUserCheck, NotifCount, ListView):
    template_name = "administration/user_management.html"
    model = User
    context_object_name = "users"
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get("name")
        if query:
            object_list = self.model.objects.filter(username__icontains=query).exclude(
                username=self.request.user
            )
        else:
            object_list = self.model.objects.exclude(username=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm
        context["users_total"] = self.get_queryset().count()

        return context


class UserDetailUpdate(LoginRequiredMixin, SuperUserCheck, NotifCount, UpdateView):
    template_name = "administration/user_detail_update.html"
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy("administration:user-management")


class UserResults(LoginRequiredMixin, SuperUserCheck, NotifCount, ListView):
    template_name = "administration/user_results.html"
    model = Profile
    context_object_name = "users"
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get("name")
        if query:
            object_list = self.model.objects.filter(
                user__username__icontains=query, is_approved__isnull=False
            ).order_by("is_approved")
        else:
            object_list = self.model.objects.exclude(is_approved=None).order_by(
                "is_approved"
            )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm
        context["users_total"] = self.get_queryset().count()

        return context


def approve_user(request):
    get_pk = request.POST["value"]
    obj = Profile.objects.get(id=get_pk)
    if obj.is_approved == True:
        obj.is_approved = False
    else:
        obj.is_approved = True
    obj.save()

    return redirect("administration:user-results")


class UserSchedules(LoginRequiredMixin, SuperUserCheck, NotifCount, ListView):
    template_name = "administration/schedules/schedules.html"
    model = AdminScheduledConsultation
    context_object_name = "users"
    paginate_by = 8

    def get_queryset(self):
        object_list = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user, is_done=False
        )

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        today = queryset.filter(scheduled_date__date=now.date())

        soon = today.filter(scheduled_date__time__gt=now.time())
        upcoming = queryset.filter(scheduled_date__date__gt=now.date())
        late = today.filter(scheduled_date__time__lt=now.time())
        history = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user, is_done=True
        )
        context["users"] = soon
        context["user_count"] = soon.count()
        context["late"] = late
        context["late_count"] = late.count()
        context["upcoming"] = upcoming
        context["upcoming_count"] = upcoming.count()
        
        context["history"] = history

        return context


class MissedSchedules(UserSchedules):
    template_name = "administration/schedules/missed.html"


class UpcomingSchedules(UserSchedules):
    template_name = "administration/schedules/upcoming.html"


class HistorySchedules(UserSchedules):
    template_name = "administration/schedules/history.html"

class ResetSchedule(LoginRequiredMixin, SuperUserCheck, UpdateView):
    template_name = "administration/schedules/reset_schedule.html"
    model = AdminScheduledConsultation
    form_class = ScheduleDateForm
    success_url = reverse_lazy("administration:schedules")