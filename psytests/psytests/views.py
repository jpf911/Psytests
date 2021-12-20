from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from accounts.models import Profile

from administration.models import AdminScheduledConsultation

import datetime
from administration.views import SuperUserCheck
from personalityTest.models import Result
from psytests.forms import ContactForm

from django.core.mail import send_mail
from django.conf import settings

from riasec.models import Riasec_result

now = datetime.datetime.today()


class HomePageView(SuperUserCheck, TemplateView):
    template_name = 'homepage.html'

    
class Assessment(LoginRequiredMixin, FormView):
    template_name = 'assessment.html'
    form_class = ContactForm
    success_url = reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['personalityTest_results']=Result.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

        try:
            context['riasec_results']=Riasec_result.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            pass

        return context


class ThankYou(LoginRequiredMixin, TemplateView):
    template_name = 'awesome.html'