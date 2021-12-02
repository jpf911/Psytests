from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy

import joblib

import pandas as pd

from personalityTest.models import Questionnaire, Result, Cluster


class PersonalityTestHomeView(LoginRequiredMixin, TemplateView):
    template_name = "personalityTest/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["results"] = Result.objects.filter(user=self.request.user)
            context["cluster1"] = Cluster.objects.get(cluster="Cluster 1")
            context["cluster2"] = Cluster.objects.get(cluster="Cluster 2")
            context["cluster3"] = Cluster.objects.get(cluster="Cluster 3")
            context["cluster4"] = Cluster.objects.get(cluster="Cluster 4")
            context["cluster5"] = Cluster.objects.get(cluster="Cluster 5")
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

        res = int(model.predict([lis])) + 1

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


class DeleteRecord(DeleteView):
    model = Result
    success_url = reverse_lazy("personalityTest:home")
    success_message = "record deleted successfully."

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteRecord, self).delete(request, *args, **kwargs)
