from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            
            # check whether username/password matches
            user = authenticate(username=data['username'], password=data['password'])
            if user :
                login(request, user)
                return redirect("post:post_list")
            else:
                return HttpResponse("Error username or password")
        else:
            return HttpResponse("Error username or password")

    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)

    else:
        return HttpResponse("GET or POST")

def user_logout(request):
    logout(request)
    return redirect("post:post_list")

# user registration
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)

        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)

            # set password
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect("post:post_list")

        else:
            return HttpResponse("Invalid form, please retry")

    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form':user_register_form }
        return render(request, 'userprofile/register.html', context)

    else:
        return HttpResponse("POST or GET")

@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # Verify user
        if request.user == user:
            # Logout and redirect to post-list
            logout(request)
            user.delete()
            return redirect("post:post_list")
        else:
            return HttpResponse("You don't have permision")
    else:
        return HttpResponse("POST only")