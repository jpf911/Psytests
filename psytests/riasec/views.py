from django.shortcuts import render
from .models import RIASEC_Test
# Create your views here.

def testPage(request):
    questions=RIASEC_Test.objects.all()
    return render(request,'riasec/test.html', {"questions":questions})

def add(request):
    r= float(request.GET.get('choices'))
    return render(request,'riasec/result.html',{'result':r})


def home(request):
    return render(request,'riasec/riasec_home.html')

