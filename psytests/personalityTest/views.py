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
from .forms import AddPQuestionsForm,AddRQuestionsForm
from django.shortcuts import get_object_or_404

import joblib

import pandas as pd

from personalityTest.models import Questionnaire, Result, Cluster
from riasec.models import RIASEC_Test


class PersonalityTestHomeView(LoginRequiredMixin, TemplateView):
    template_name = "personalityTest/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["cluster1"] = Cluster.objects.get(cluster="Cluster 1")
            context["cluster2"] = Cluster.objects.get(cluster="Cluster 2")
            context["cluster3"] = Cluster.objects.get(cluster="Cluster 3")
            context["cluster4"] = Cluster.objects.get(cluster="Cluster 4")
            context["cluster5"] = Cluster.objects.get(cluster="Cluster 5")
            context["results"] = Result.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass
        
        
        return context


class TestView(LoginRequiredMixin, TemplateView):
    template_name = "personalityTest/testPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Questionnaire.objects.all()
        return context

    def post(self, *args, **kwargs):
        name = self.request.user
        model = joblib.load("model/theModel.sav")
        q = Questionnaire.objects.all().order_by('pk').values_list('id', flat=True)
        lis = []
        ext = []
        est = []
        agr = []
        csn = []
        opn = []

        for id in q.iterator():
            score = float(self.request.POST.get(f"{id}"))
            question = Questionnaire.objects.get(pk=id)

            lis.append(score)

            if question.category == "EXT":
                ext.append(score)
            if question.category == "EST":
                est.append(score)
            if question.category == "AGR":
                agr.append(score)
            if question.category == "CSN":
                csn.append(score)
            if question.category == "OPN":
                opn.append(score)

        res = int(model.predict([lis])) + 1

        if res == 1:
            res = Cluster.objects.get(cluster='Cluster 1')
        if res == 2:
            res = Cluster.objects.get(cluster='Cluster 2')
        if res == 3:
            res = Cluster.objects.get(cluster='Cluster 3')
        if res == 4:
            res = Cluster.objects.get(cluster='Cluster 4')
        if res == 5:
            res = Cluster.objects.get(cluster='Cluster 5')

        df = pd.DataFrame(lis).transpose()

        # my_sums = pd.DataFrame()
        extroversion = df[ext].sum(axis=1) / 10
        neurotic = df[est].sum(axis=1) / 10
        agreeable = df[agr].sum(axis=1) / 10
        conscientious = df[csn].sum(axis=1) / 10
        openness = df[opn].sum(axis=1) / 10

        try:
            obj = Result.objects.get(user=name)
            obj.user = name
            obj.prediction = res
            obj.extroversion = extroversion
            obj.neurotic = neurotic
            obj.agreeable = agreeable
            obj.conscientious = conscientious
            obj.openness = openness
            obj.save()

        except ObjectDoesNotExist:
            result = Result.objects.create(
                user=name,
                prediction=res,
                extroversion=extroversion,
                neurotic=neurotic,
                agreeable=agreeable,
                conscientious=conscientious,
                openness=openness,
            )
            result.save()

        return HttpResponseRedirect(reverse("personalityTest:home"))


class DeleteRecord(LoginRequiredMixin,DeleteView):
    model = Result
    success_url = reverse_lazy("personalityTest:home")
    success_message = "record deleted successfully."

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteRecord, self).delete(request, *args, **kwargs)

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

class QuestionsListView(SuperUserCheck,TemplateView):

    model = Questionnaire, RIASEC_Test
    template_name = "questions/questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pquestions'] = Questionnaire.objects.all()
        context['rquestions'] = RIASEC_Test.objects.all()
        return context

class RQuestionsDetailView(SuperUserCheck, DetailView):
    model = RIASEC_Test
    template_name = "questions/rquestions_detail.html"
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #post= RIASEC_Test.objects.filter(slug=self.kwargs.get('slug'))
        return context

class PQuestionsDetailView(SuperUserCheck, DetailView):
    model = Questionnaire
    template_name = "questions/pquestions_detail.html"
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post= Questionnaire.objects.filter(slug=self.kwargs.get('slug'))
        return context

class RQuestionsCreateView(UserAccessMixin, CreateView):
    permission_required = 'can_create'
    model =RIASEC_Test
    form_class = AddRQuestionsForm
    template_name = 'questions/rquestions_add.html'
    success_url = reverse_lazy('personalityTest:questions')

    def form_valid(self, form):
        return super(RQuestionsCreateView, self).form_valid(form)

class PQuestionsCreateView(UserAccessMixin,CreateView):
    permission_required = 'can_create'
    model = Questionnaire
    form_class = AddPQuestionsForm
    template_name = 'questions/pquestions_add.html'
    success_url = reverse_lazy('personalityTest:questions')

    def form_valid(self, form):
        return super(PQuestionsCreateView, self).form_valid(form)


class RQuestionsEditView(UserAccessMixin,UpdateView):
    permission_required = 'can_edit'
    model=RIASEC_Test
    form_class = AddRQuestionsForm
    template_name = 'questions/rquestions_add.html'
    success_url = reverse_lazy('personalityTest:questions')

class PQuestionsEditView(UserAccessMixin, UpdateView):
    permission_required = 'can_edit'
    model= Questionnaire
    form_class = AddPQuestionsForm
    template_name = 'questions/pquestions_add.html'
    success_url = reverse_lazy('personalityTest:questions')


class RDeleteQuestions(UserAccessMixin,DeleteView):
    permission_required = 'can_delete'
    model = RIASEC_Test
    success_message = "question deleted successfully."
    success_url = reverse_lazy("personalityTest:questions")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(RDeleteQuestions, self).delete(request, *args, **kwargs)

class PDeleteQuestions(UserAccessMixin, DeleteView):
    permission_required = 'can_delete'
    model = Questionnaire
    success_message = "question deleted successfully."
    success_url = reverse_lazy("personalityTest:questions")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PDeleteQuestions, self).delete(request, *args, **kwargs)