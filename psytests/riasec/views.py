from django.shortcuts import render
from django.urls import reverse
from django.http import  HttpResponseRedirect
from .models import RIASEC_Test
# Create your views here.

def testPage(request):
    questions=RIASEC_Test.objects.all()
    return render(request,'riasec/test.html', {"questions":questions})

def evaluate(request,question_id):
    if request.method == 'POST':
        score = (request.POST.get(pk=question_id))
        r = []
        i = []
        a = []
        s = []
        e = []
        c = []

        if score.category == 'Reality':
            r.append(request.POST.get(score))
        if score.category == 'Investigative':
            i.append(request.POST.get(score))
        if score.category == 'Artistic':
            a.append(request.POST.get(score))
        if score.category == 'Social':
            s.append(request.POST.get(score))
        if score.category == 'Enterprising':
            e.append(request.POST.get(score))
        if score.category == 'Conventional':
            c.append(request.POST.get(score))

        # i= float(request.POST.getlist('I'))
        # a= float(request.POST.getlist('A'))
        # s= float(request.POST.getlist('S'))
        # e= float(request.POST.getlist('E'))
        # c= float(request.POST.getlist('C'))

        print(r)
        return HttpResponseRedirect(reverse('riasec:riasec_home'))
    # return render(request,'riasec/result.html',{'r':r,'i':i,'a':a,'s':s,'e':e,'c':c})

def home(request):
    return render(request,'riasec/riasec_home.html')

