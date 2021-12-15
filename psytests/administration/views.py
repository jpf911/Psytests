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
from .forms import SearchForm,AddRQuestionsForm,AddPQuestionsForm
from personalityTest.models import Questionnaire,Result
from riasec.models import RIASEC_Test,Riasec_result
from accounts.models import Profile
from accounts.forms import UpdateUserForm


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

class UserDetailView(SuperUserCheck, TemplateView):
    template_name = 'administration/admin/users_detail.html'
    model = Riasec_result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['riasec_results'] = Riasec_result.objects.filter(pk=self.kwargs.get('pk'))
            context['personalityTest_results'] = Result.objects.filter(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            pass
        return context
