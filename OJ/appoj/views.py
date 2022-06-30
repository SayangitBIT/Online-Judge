from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from appoj.models import UserProfile


# def index(request):
#     #template = loader.get_template('appoj/index.html')
#     return render(request, 'appoj/index.html')


class login_view(View):
    def get(self, request):
        return render(request, 'appoj/login.html')
    def post(self, request):
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/appoj/problems')
        else:
            return HttpResponse("invalid user")

class register(View):
    def get(self, request):
        return render(request, 'appoj/register.html')
    def post(self, request):
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is None:
            newuser = User.objects.create_user(username = request.POST['username'], password = request.POST['password'], email = request.POST['email'])
            # print(request.POST['username'])
            newuserprofile = UserProfile(user = newuser)
            newuser.save()
            newuserprofile.save()
            return HttpResponse("registered successfully")
        else:
            return HttpResponse("User already present!")

@login_required(login_url = '/appoj/')
def problems(request):
    # print(request.user.username)
    return HttpResponse("You're looking at problems list.")

@login_required(login_url = '/appoj/')
def logout_view(request):
    logout(request)
    print("logging out")
    return redirect('/appoj/')