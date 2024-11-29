from django.shortcuts import render,redirect
from .forms import Sign_up,Log_in,Reset_pass,Check_id,Login_employee
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from users.models import Person
from users.views import main,user_is_logined,add_person_information
from documents.views import show_documents
from django.http import HttpResponse

def check_pass(request):
    try :
        task_name = 'reset password'
        error=' '
        if request.method == "POST":
            data = Reset_pass(request.POST)
            if data.is_valid():
                new_password = request.POST['new_password']
                confirm_password = request.POST['confirm_password']
                if new_password == confirm_password :
                    user = request.user
                    user.password  = new_password
                    user.save()
                    return redirect(main)
                else:
                    error = 'the passwords not match'
            else:
                error = data.errors
        return render(request,'registering/pass.html',{'form':Reset_pass,'error':error,'task_name':task_name}) 
    except:
        return HttpResponse('sorry there is an error please try another thing')

def reset_pass(request):
    try :
        task_name = 'type id'
        error=' '
        if request.method == "POST":
            data = Check_id(request.POST)
            if data.is_valid():
                person = Person.objects.get(person_name=request.user.username)
                national_num = person.national_num
                current_national_num = request.POST['national_num']
                if national_num == current_national_num :
                    return redirect(check_pass)
                else:
                    error = 'wrong id'
            else:
                error = data.errors
        return render(request,'registering/pass.html',{'form':Check_id,'error':error,'task_name':task_name})    
    except:
        return HttpResponse('sorry there is an error please try another thing')

def log_out(request):
    logout(request)
    try :
        del request.session['employee']
    except:
        pass
    return redirect('log_in')
 
def log_in(request):
    try :
        error=' '
        task_name = 'login'
        if request.method == "POST":
            data = Log_in(request.POST)
            if data.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user =  authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    if Person.objects.filter(person_name=username).exists():
                        return redirect(main)
                    else :
                        return redirect(add_person_information)         
            else:
                error = data.errors
        return render(request,'registering/login.html',{'user':Log_in,'error':error,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def sign_up(request):
    try :
        error=' '
        task_name = 'signup'
        if request.method == "POST":
            data = Sign_up(request.POST)
            if data.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                if user is not None:
                    login(request,user)
                    if Person.objects.filter(person_name=username).exists():
                        return redirect(main)
                    else :
                        return redirect(add_person_information)
            else:
                error = data.errors
        return render(request,'registering/login.html',{'user':Sign_up,'error':error,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def login_employee(request):
    try :
        task_name = 'login as employee'
        error = 'assert 12345'
        if request.session.get('employee','00000000000') != '00000000000' :
            del request.session['employee']
            request.user.is_staff = False
            return redirect(main)
        if request.method == "POST":
            password = request.POST['password']
            if password == '12345' :
                name = user_is_logined(request=request)
                request.session['employee'] = name
                request.user.is_staff = True
                return redirect(show_documents)
            else :
                error = 'wrong password assert 12345'
        return render(request,'registering/pass.html',{'form':Login_employee,'error':error,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')
   
