from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView

from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy


import joblib
import pandas as pd
from accounts.models import Profile

from personalityTest.models import Questionnaire, Result, Cluster
from riasec.models import Riasec_result


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

        try:
            context['existed'] = Result.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

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

            if question.key == '0':
                if score == 5:
                    score = 1
                if score == 4:
                    score = 2

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

            lis.append(score)
            print(question.key)

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

        try:
            obj = Result.objects.get(user__username=name)
            obj2 = Riasec_result.objects.get(user__username=name)

            if obj and obj2:
                obj3 = Profile.objects.get(user__username=name)
                obj3.is_assigned = False
                obj3.save()
        except ObjectDoesNotExist:
            pass

        return redirect('awesome')

class ResultView(LoginRequiredMixin, TemplateView):
    template_name = "personalityTest/resultPage.html"

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

        try:
            context['personalityTest_result'] = Result.objects.get(user=self.request.user)
            obj_prediction = Result.objects.get(user=self.request.user)
            context['prediction'] = obj_prediction.prediction
        except ObjectDoesNotExist:
            pass
        
        return context
