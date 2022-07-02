from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from appoj.models import UserProfile, Problems, Verdicts


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
    _Problems = Problems.objects.all()
    dux = {}
    for x in _Problems:
        #send either the object itself or the primary key of the referenced model when using get with foreignkey
        print(request.user.username)
        is_present = Verdicts.objects.filter(problem_id = x, user_id = UserProfile.objects.get(user__username = request.user.username)).exists()

        if is_present:
            curuser = Verdicts.objects.get(problem_id = x, user_id = UserProfile.objects.get(user__username = request.user.username))
            dux.update({x.problem_id : [x.name, x.difficulty, curuser.solved_status]})
        else:
            newuser = UserProfile.objects.get(user__username = request.user.username)
            _newuser = Verdicts(problem_id = x, user_id = newuser, solved_status = "no")
            _newuser.save()
            dux.update({x.problem_id : [x.name, x.difficulty, "no"]})
        
    # print(dux[1])
    context = {'context' : dux}
    # return HttpResponse("You're looking at problems list.")
    return render(request, 'appoj/problems.html', context)

@login_required(login_url = '/appoj/')
def to_problems(request, p_no):
    curproblem = Problems.objects.filter(problem_id = p_no).values().first()
    dux = Problems.objects.get(problem_id = p_no)
    l = {'chicken' : "a \nb"}
    # print(l["chicken"])
    #print(dux.sample_input)
    return render(request, 'appoj/display_problem.html', {'question': dux})

@login_required(login_url = '/appoj/')
def logout_view(request):
    logout(request)
    print("logging out")
    return redirect('/appoj/')