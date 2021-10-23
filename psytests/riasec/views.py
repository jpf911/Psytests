from django.shortcuts import render, reverse
from django.http import  HttpResponseRedirect
from .models import RIASEC_Test, Riasec_result
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url='/psytest/login')
def testPage(request):
    questions=RIASEC_Test.objects.all()
    return render(request,'riasec/test.html', {"questions":questions})

def evaluate(request):
    r = []
    i = []
    a = []
    s = []
    e = []
    c = []
    
    for id in range(1,43):
        score = request.POST.get(f'{id}')
        question = RIASEC_Test.objects.get(pk=id)
        get_score=request.POST.get(score)
        # print(f'{question} = {get_score}')

        if get_score is not None:
            get_score=float(get_score)
            if question.category == 'R':
                r.append(get_score)
            if question.category == 'I':
                i.append(get_score)
            if question.category == 'A':
                a.append(get_score)
            if question.category == 'S':
                s.append(get_score)
            if question.category == 'E':
                e.append(get_score)
            if question.category == 'C':
                c.append(get_score)

    r = sum(r)
    i = sum(i)
    a = sum(a)
    s = sum(s)
    e = sum(e)
    c = sum(c)
    name=request.user
    result = Riasec_result.objects.update(user=name,reality=r, investigative=i, artistic=a, social=s,enterprising=e, conventional=c)
    result.save()
    return HttpResponseRedirect(reverse('riasec:home'))

def home(request):
    return render(request,'riasec/riasec_home.html')

