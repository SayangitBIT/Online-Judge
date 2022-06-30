from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from appoj.models import UserProfile

# def index(request):
#     #template = loader.get_template('appoj/index.html')
#     return render(request, 'appoj/index.html')


class login(View):
    def get(self, request):
        return render(request, 'appoj/login.html')
    def post(self, request):
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is not None:
            return HttpResponse("submitted yay!")
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
    
def problems(request):
    return HttpResponse("You're looking at problems list.")