from django.shortcuts import render
# Create your views here.

def testPage(request):
    return render(request,'riasec/test.html')

