from django.shortcuts import render, reverse
from django.http import  HttpResponseRedirect
from .models import RIASEC_Test, Riasec_result
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

    r = sum(r)
    i = sum(i)
    a = sum(a)
    s = sum(s)
    e = sum(e)
    c = sum(c)
    name=request.user
    result = Riasec_result.objects.update(user=name,reality=r, investigative=i, artistic=a, social=s,enterprising=e, conventional=c)
    return HttpResponseRedirect(reverse('riasec:home'))

def home(request):
    return render(request,'riasec/riasec_home.html')

