from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from .forms import CreateUserForm
from .decorators import unauthenticated_user
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
            user.profile.birth_date = form.cleaned_data.get('date_of_birth')
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