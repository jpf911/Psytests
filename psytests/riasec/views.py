from django.shortcuts import render, reverse
from django.http import  HttpResponseRedirect
from .models import RIASEC_Test, Riasec_result
from django.contrib.auth.models import User
# Create your views here.

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
        print('This is question', question)


        if question.category == 'R':
            r.append(int(request.POST.get(score)))
        if question.category == 'I':
            i.append(int(request.POST.get(score)))
        if question.category == 'A':
            a.append(int(request.POST.get(score)))
        if question.category == 'S':
            s.append(int(request.POST.get(score)))
        if question.category == 'E':
            e.append(int(request.POST.get(score)))
        if question.category == 'C':
            c.append(int(request.POST.get(score)))

    print(r)
    r = sum(r)
    i = sum(i)
    a = sum(a)
    s = sum(s)
    e = sum(e)
    c = sum(c)


    result = Riasec_result.objects.create(user=request.user, reality=r, investigative=i, artistic=a, social=s, enterprising=e, conventional=c)
    result.save()

    return HttpResponseRedirect(reverse('riasec:home'))

def home(request):
    return render(request,'riasec/riasec_home.html')

