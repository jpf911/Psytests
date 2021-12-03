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
from .forms import AddQuestionsForm
from django.shortcuts import get_object_or_404

import joblib

import pandas as pd

from personalityTest.models import Questionnaire, Result, Cluster


class PersonalityTestHomeView(LoginRequiredMixin, TemplateView):
    template_name = "personalityTest/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = Result.objects.all()
        return context


class TestView(LoginRequiredMixin, TemplateView):
    template_name = "personalityTest/testPage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Questionnaire.objects.all()
        return context
    
    def post(self, *args, **kwargs):
        name = self.request.user
        model = joblib.load("model/theModel.sav")

        lis = []
        ext = []
        est = []
        agr = []
        csn = []
        opn = []

        for id in range(1, 51):
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

        res = model.predict([lis])

        df = pd.DataFrame(lis).transpose()

        # my_sums = pd.DataFrame()
        extroversion = df[ext].sum(axis=1)/10
        neurotic = df[est].sum(axis=1)/10
        agreeable = df[agr].sum(axis=1)/10
        conscientious = df[csn].sum(axis=1)/10
        openness = df[opn].sum(axis=1)/10


        try:
            Result.objects.get(user=name)
            Result.objects.filter(user=name).update(
                user=name,
                prediction = int(res),
                extroversion=extroversion,
                neurotic=neurotic,
                agreeable=agreeable,
                conscientious=conscientious,
                openness=openness,
            )

        except ObjectDoesNotExist:
            result = Result.objects.create(
                user=name,
                prediction = int(res),
                extroversion=extroversion,
                neurotic=neurotic,
                agreeable=agreeable,
                conscientious=conscientious,
                openness=openness,
            )
            result.save()

        return HttpResponseRedirect(reverse("personalityTest:home"))

class DeleteRecord(DeleteView):
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

class QuestionsListView(SuperUserCheck,ListView):

    model = Questionnaire
    template_name = "personalityTest/questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Questionnaire.objects.all()
        return context


class QuestionsDetailView(SuperUserCheck,DetailView):
    model = Questionnaire
    template_name = "personalityTest/questions_detail.html"
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post= Questionnaire.objects.filter(slug=self.kwargs.get('slug'))

        return context

class QuestionsCreateView(LoginRequiredMixin,CreateView):
    model = Questionnaire
    form_class = AddQuestionsForm
    template_name = 'personalityTest/questions_add.html'
    success_url = reverse_lazy('personalityTest:questions')

    def form_valid(self, form):
        return super(QuestionsCreateView, self).form_valid(form)


class QuestionsEditView(LoginRequiredMixin,UpdateView):
    model= Questionnaire
    form_class = AddQuestionsForm
    template_name = 'personalityTest/questions_add.html'
    success_url = reverse_lazy('personalityTest:questions')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(QuestionsEditView, self).form_valid(form)

class DeleteQuestions(LoginRequiredMixin,DeleteView):
    model = Questionnaire
    success_message = "question deleted successfully."
    success_url = reverse_lazy("personalityTest:questions")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteQuestions, self).delete(request, *args, **kwargs)