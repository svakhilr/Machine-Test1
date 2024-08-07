from users.models import UserProfile
from django.shortcuts import render,redirect
from .forms import UserLoginForm
from django.contrib.auth import  login,logout
from django.contrib.auth import authenticate
import sweetify






def admin_login(request):
    if request.method == "POST":
        print("username",request.POST)
        form = UserLoginForm(request.POST)
        username =request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        
        if user:
            # return redirect("users-list")
            if user.is_staff:
                login(request,user)
                sweetify.success(request, 'Welcome')
                return redirect("users-list")
        else:
            sweetify.warning(request, 'Invalid Credentials')
    form = UserLoginForm()
    return render(request,'login.html',{'form':form})

def users_list(request):
    if not request.user.is_authenticated and not request.user.is_staff:
        return redirect("admin-login")
    
    
    
    users  = UserProfile.objects.filter(user__is_staff=False)
    context = {
        "users":users
    }
    return render(request, 'users.html',context)

    



        