from django.views.generic.base import TemplateView, View
from accounts.models import Profile

from administration.models import AdminScheduledConsultation

import datetime

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
            scheduled_date__date=now.date(),
            scheduled_date__time__lt=now.time()
        ).count()
        context["notif_count"] =  notif_count if notif_count is not None else None

        return context


class HomePageView(NotifCount, TemplateView):
    template_name = 'homepage.html'

    

