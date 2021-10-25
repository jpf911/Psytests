from django.shortcuts import render, reverse
from django.http import  HttpResponseRedirect
from .models import RIASEC_Test, Riasec_result
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@login_required(login_url='accounts:login')
def testPage(request):
    y = 1
    x = 0
    questions=RIASEC_Test.objects.all()
    return render(request,'riasec/test.html', {
        "questions":questions,
        'x': x,
        'y': y,
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

    if(Riasec_result.objects.get(user=name)):
        Riasec_result.objects.update(user=name,reality=r, investigative=i, artistic=a, social=s,enterprising=e, conventional=c)
    else:
        result=Riasec_result.objects.create(user=name,reality=r, investigative=i, artistic=a, social=s,enterprising=e, conventional=c)
        result.save()

    return HttpResponseRedirect(reverse('riasec:home'))
class Home(ListView):
    model = Riasec_result
    template_name = 'riasec/riasec_home.html'
    context_object_name = 'results'

    def get_queryset(self):
        result = Riasec_result.objects.filter(user=self.request.user)
        return result