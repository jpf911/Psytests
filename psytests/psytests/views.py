from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView
from accounts.models import Profile

from administration.models import AdminScheduledConsultation

import datetime
from personalityTest.models import Result

from riasec.models import Riasec_result

now = datetime.datetime.today()

class NotifCount():

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unapproved_users'] = Profile.objects.filter(is_approved=False).count()
        notif_count = AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user,
            is_done=False,
            scheduled_date__date=now.date(),
            scheduled_date__time__gt=now.time()
        ).count() + AdminScheduledConsultation.objects.filter(
            managed_by__user=self.request.user,
            is_done=False,
            scheduled_date__lt=now.today()
        ).count()
        context["notif_count"] =  notif_count if notif_count is not None else None

        return context


class HomePageView(NotifCount, TemplateView):
    template_name = 'homepage.html'

    
class Assessment(LoginRequiredMixin, NotifCount, TemplateView):
    template_name = 'assessment.html'

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