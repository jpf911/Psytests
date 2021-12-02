from django.shortcuts import render,redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreateUserForm
from .decorators import unauthenticated_user

from riasec.models import Riasec_result
from personalityTest.models import Result
# Create your views here.

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request,'accounts/login.html')

@unauthenticated_user
def registerPage(request):
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.profile.gender = form.cleaned_data.get('gender')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request,'accounts/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('accounts:login')

class StatPage(TemplateView):
    template_name = 'stats/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['personalityTest_result'] = Result.objects.get(user=self.request.user)
            context['riasec_result'] = Riasec_result.objects.get(user=self.request.user)
            Riasec_result.objects.get(user=self.request.user)
            obj = Riasec_result.objects.filter(user=self.request.user).values(
                "realistic",
                "investigative",
                "artistic",
                "social",
                "enterprising",
                "conventional",
            ).first()
            if obj is not None:
                objects = dict(sorted(obj.items(), key=lambda item: item[1], reverse=True))
                top1 = {}
                top2 = {}
                top3 = {}
                for x in objects:
                    if not top1:
                        top1[x] = objects[x]
                    else:
                        if objects[x] == list(top1.values())[0]:
                            top1[x] = objects[x]
                        if top2:
                            if objects[x] < list(top2.values())[0] and not top3:
                                top3[x] = objects[x]
                                continue
                        if objects[x] < list(top1.values())[0] and not top3:
                            top2[x] = objects[x]
                        if top3:
                            if objects[x] == list(top3.values())[0]:
                                top3[x] = objects[x]
                context["top1"] = top1
                context["top2"] = top2
                context["top3"] = top3
                if top1:
                    context["top1value"] = list(top1.values())[0]
                if top2:
                    context["top2value"] = list(top2.values())[0]
                if top3:
                    context["top3value"] = list(top3.values())[0] 
        except ObjectDoesNotExist:
            pass

        

        return context