from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import  HttpResponseRedirect
from .models import RIASEC_Test, Riasec_result
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages



# Create your views here.

@login_required(login_url='accounts:login')
def testPage(request):
    range_num = range(42)
    obj = Riasec_result.objects.all()
    questions=RIASEC_Test.objects.all()
    return render(request,'riasec/test.html', {
        "questions":questions,
        'obj': obj,
        'range': range_num
        })


def evaluate(request):
    r = []
    i = []
    a = []
    s = []
    e = []
    c = []

    for id in range(1,43):
        score = float(request.POST.get(f'{id}'))
        question = RIASEC_Test.objects.get(pk=id)

        if question.category == 'R':
            r.append(score)
        if question.category == 'I':
            i.append(score)
        if question.category == 'A':
            a.append(score)
        if question.category == 'S':
            s.append(score)
        if question.category == 'E':
            e.append(score)
        if question.category == 'C':
            c.append(score)

    r = (sum(r)/7) * 100
    i = (sum(i)/7) * 100
    a = (sum(a)/7) * 100
    s = (sum(s)/7) * 100
    e = (sum(e)/7) * 100
    c = (sum(c)/7) * 100
    name=request.user

    try:
        Riasec_result.objects.get(user=request.user)
        Riasec_result.objects.update(user=name,reality=r, investigative=i, artistic=a, social=s,enterprising=e, conventional=c)
    
    except ObjectDoesNotExist:
        result=Riasec_result.objects.create(user=name,reality=r, investigative=i, artistic=a, social=s,enterprising=e, conventional=c)
        result.save()

    return HttpResponseRedirect(reverse('riasec:home'))


class Home(LoginRequiredMixin,ListView):
    model = Riasec_result
    template_name = 'riasec/riasec_home.html'
    context_object_name = 'result'

    def get_queryset(self):
        result = Riasec_result.objects.filter(user=self.request.user)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Riasec_result.objects.values('reality', 'investigative', 'artistic', 'social', 'enterprising', 'conventional').first()
        if obj is not None:
            sorted_obj = dict(sorted(obj.items(), key=lambda item: item[1]))
            first_three_obj = dict(list(sorted_obj.items())[:2:-1])
            context['ranks'] = first_three_obj
        return context

class DeleteRecord(LoginRequiredMixin,DeleteView):
    model = Riasec_result
    success_url = reverse_lazy('riasec:home')
    success_message = "record deleted successfully."

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteRecord, self).delete(request, *args, **kwargs)