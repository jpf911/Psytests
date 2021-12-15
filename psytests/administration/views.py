from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist
from django.forms import fields
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

from personalityTest.models import Questionnaire,Result
from riasec.models import RIASEC_Test,Riasec_result

from psytests.views import NotifCount

from datetime import datetime

from .forms import ScheduleDateForm, SearchForm, AddRQuestionsForm, AddPQuestionsForm
from .models import AdminScheduledConsultation

from accounts.models import Profile
from accounts.forms import UpdateUserForm

now = datetime.today()

# Create your views here.
class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return  redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('')
        return super(UserAccessMixin,self).dispatch(request,*args,**kwargs)


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

    return redirect('administration:user-results')

class RQuestionsTemplateView(SuperUserCheck,TemplateView):

    model =RIASEC_Test
    template_name = "administration/questions/rquestions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rquestions'] = RIASEC_Test.objects.all()
        return context

class PQuestionsTemplateView(SuperUserCheck,TemplateView):

    model = Questionnaire
    template_name = "administration/questions/pquestions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pquestions'] = Questionnaire.objects.all()
        return context

class RQuestionsDetailView(SuperUserCheck, DetailView):
    model = RIASEC_Test
    template_name = "administration/rquestions/rquestions_detail.html"
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #post= RIASEC_Test.objects.filter(slug=self.kwargs.get('slug'))
        return context

class PQuestionsDetailView(SuperUserCheck, DetailView):
    model = Questionnaire
    template_name = "administration/pquestions/pquestions_detail.html"
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post= Questionnaire.objects.filter(slug=self.kwargs.get('slug'))
        return context

class RQuestionsCreateView(UserAccessMixin, CreateView):
    permission_required = 'can_create'
    model =RIASEC_Test
    form_class = AddRQuestionsForm
    template_name = 'administration/questions/rquestions_add.html'
    success_url = reverse_lazy('administration:rquestions')

    def form_valid(self, form):
        return super(RQuestionsCreateView, self).form_valid(form)

class PQuestionsCreateView(UserAccessMixin,CreateView):
    permission_required = 'can_create'
    model = Questionnaire
    form_class = AddPQuestionsForm
    template_name = 'administration/questions/pquestions_add.html'
    success_url = reverse_lazy('administration:pquestions')

    def form_valid(self, form):
        return super(PQuestionsCreateView, self).form_valid(form)

class RQuestionsEditView(UserAccessMixin,UpdateView):
    permission_required = 'can_edit'
    model=RIASEC_Test
    form_class = AddRQuestionsForm
    template_name = 'administration/questions/rquestions_add.html'
    success_url = reverse_lazy('administration:rquestions')

class PQuestionsEditView(UserAccessMixin, UpdateView):
    permission_required = 'can_edit'
    model= Questionnaire
    form_class = AddPQuestionsForm
    template_name = 'administration/questions/pquestions_add.html'
    success_url = reverse_lazy('administration:pquestions')


class RDeleteQuestions(UserAccessMixin,DeleteView):
    permission_required = 'can_delete'
    model = RIASEC_Test
    success_message = "question deleted successfully."
    success_url = reverse_lazy("administration:rquestions")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(RDeleteQuestions, self).delete(request, *args, **kwargs)

class PDeleteQuestions(UserAccessMixin, DeleteView):
    permission_required = 'can_delete'
    model = Questionnaire
    success_message = "question deleted successfully."
    success_url = reverse_lazy("administration:pquestions")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PDeleteQuestions, self).delete(request, *args, **kwargs)

class UsersResults(SuperUserCheck, TemplateView):
    template_name = 'administration/admin/results.html'
    model = Riasec_result, Result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['riasec_result'] = Riasec_result.objects.all()
            context['personalityTest_result'] = Result.objects.all()
        except ObjectDoesNotExist:
            pass
        return context

class UserDetailView(SuperUserCheck, DetailView):
    template_name = 'administration/admin/users_detail.html'
    model = Riasec_result
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['riasec_results'] = Riasec_result.objects.get(id=self.kwargs.get('pk'))
            Riasec_result.objects.get(id=self.kwargs.get('pk'))
            obj = Riasec_result.objects.filter(id=self.kwargs.get('pk')).values(
                "realistic",
                "investigative",
                "artistic",
                "social",
                "enterprising",
                "conventional",
            ).first()
            if obj is not None:
                objects = dict(sorted(obj.items(), key=lambda item: item[1], reverse=True))
                top1 = {}
                top2 = {}
                top3 = {}
                for x in objects:
                    if not top1:
                        top1[x] = objects[x]
                    else:
                        if objects[x] == list(top1.values())[0]:
                            top1[x] = objects[x]
                        if top2:
                            if objects[x] < list(top2.values())[0] and not top3:
                                top3[x] = objects[x]
                                continue
                        if objects[x] < list(top1.values())[0] and not top3:
                            top2[x] = objects[x]
                        if top3:
                            if objects[x] == list(top3.values())[0]:
                                top3[x] = objects[x]
                context["top1"] = top1
                context["top1len"] = range(len(top1))
                context["top2"] = top2
                context["top2len"] = range(len(top2))
                context["top3"] = top3
                context["top3len"] = range(len(top3))
                if top1:
                    context["top1value"] = list(top1.values())[0]
                if top2:
                    context["top2value"] = list(top2.values())[0]
                if top3:
                    context["top3value"] = list(top3.values())[0]
        except ObjectDoesNotExist:
            pass

        try:
            context['personalityTest_results'] = Result.objects.get(id=self.kwargs.get('pk'))
            obj_prediction = Result.objects.get(id=self.kwargs.get('pk'))
            context['prediction'] = obj_prediction.prediction
        except ObjectDoesNotExist:
            pass

        return context


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
