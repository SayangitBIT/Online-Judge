from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from appoj.models import UserProfile, Problems, Verdicts, TestCases, Submissions
from glob import glob
import subprocess


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

# @login_required(login_url = '/appoj/')
class to_problems(LoginRequiredMixin, View):
    login_url = '/appoj/'
    def get(self, request, p_no):
        curproblem = Problems.objects.filter(problem_id = p_no).values().first()
        dux = Problems.objects.get(problem_id = p_no)
        print(dux.problem_id)
        return render(request, 'appoj/display_problem.html', {'question': dux})

    def post(self, request, p_no):
        problem_sol = request.POST['problem_sol']
        test_object = TestCases.objects.get(problem_id = p_no)
        

        cpp_lang = open("C:/Users/Lenovo/OneDrive - Birla Institute of Technology/Desktop/C.cpp","w+")
        cpp_lang.write(problem_sol)
        cpp_lang.close()

        ##Might comment the below lines from 83 to 89 later
        with open("C:/Users/Lenovo/OneDrive - Birla Institute of Technology/Desktop/C.cpp", 'r') as file :
            filedata = file.read()
        # Replace the target string
        filedata = filedata.replace('\n\n', '\n')
        # Write the file out again
        with open("C:/Users/Lenovo/OneDrive - Birla Institute of Technology/Desktop/C.cpp", 'w') as file:
            file.write(filedata)
        
        process = subprocess.run('g++ C:/Users/Lenovo/"OneDrive - Birla Institute of Technology"/Desktop/C.cpp -o otx' , shell=True, capture_output=True, text=True)
        procesd = subprocess.run(['otx', '<',  test_object.input], shell=True, capture_output=True, text=True)

        _user_id = UserProfile.objects.get(user__email = request.user.email)
        _status = Verdicts.objects.get(problem_id_id = p_no, user_id = _user_id)
        
        #print(procesd.stdout)
        if procesd.stdout.strip() == open(test_object.output).read():
            if (_status.solved_status != "AC"):
                _status.solved_status = "AC"
                _status.save()
            print('Success')
            Submissions(problem_id_id = p_no, user_id = _user_id, vrt = "AC").save()
        else:
            if (_status.solved_status != "AC" and _status.solved_status != "WA"):
                _status.solved_status = "WA"
                _status.save()
            print('Fail')
            Submissions(problem_id_id = p_no, user_id = _user_id, vrt = "WA").save()
        return redirect('/appoj/submissions')


@login_required(login_url = '/appoj/')
def submissions_view(request):
    dux = Submissions.objects.all()
    tux = Problems.objects.all()
    print(dux)
    print(tux)
    return render(request, 'appoj/submissions.html', {'question': dux})

@login_required(login_url = '/appoj/')
def logout_view(request):
    logout(request)
    print("logging out")
    return redirect('/appoj/')