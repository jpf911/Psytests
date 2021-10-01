from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from .forms import CreateUserForm
from .decorators import unauthenticated_user,allowed_users,admin_only
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
    context={}
    return render(request,'psytest/login.html',context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username') #Get Username

            group=Group.objects.get(name='client')
            user.groups.add(group)

            messages.success(request, 'Account was created for' + username) #Show Success message
            return redirect('login')

    context = {'form': form}
    return render(request,'psytest/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('psytest:login')

# @login_required(login_url='psytest/login')
# @admin_only
def home(request):
    return render(request,'psytest/homepage.html')