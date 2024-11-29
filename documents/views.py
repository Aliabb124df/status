from django.shortcuts import render,redirect
from users.views import get_family,get_by_obj,get_marrid,get_first_relation,user_is_logined,get_divorce,main
from users.models import Person,Marrid,Divorce,Dead,TaskPerson
from .forms import Dead_register,Send_notes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Document
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse

def send_email_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = [request.POST.get('email')]

        try:
            print('1')
            print(settings.DEFAULT_FROM_EMAIL)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            messages.success(request, 'تم إرسال البريد الإلكتروني بنجاح!')
            return redirect('family_doc')  # استبدلها بالعنوان URL المطلوب
        except Exception as e:
            er = messages.error(request, f'حدث خطأ: {e}')
            print(er)

    return render(request, 'mail/mail.html')

def get_person(request):
        name = user_is_logined(request=request)
        logged_person = request.session.get('employee','0')
        if logged_person =='0':
            if Person.objects.filter(person_name=name).exists() :
                person = Person.objects.get(person_name=name)
            elif TaskPerson.objects.filter(person_name=name).exists() :
                person = TaskPerson.objects.get(person_name=name,code=None)
            
        else :
            document_code = request.session.get('document_code','0')
            document = Document.objects.get(code=document_code)
            person_national_num =document.person_national_num
            if Person.objects.filter(national_num=person_national_num).exists() :
                person = Person.objects.get(national_num=person_national_num)
            elif TaskPerson.objects.filter(national_num=person_national_num).exists() :
                person = TaskPerson.objects.get(national_num=person_national_num,code=None)
        return person

def refuse_with_note(request):
    try :
        name = user_is_logined(request=request)
        error = ''
        task_name = 'refuse with note'
        if request.method == "POST":
            data = Send_notes(request.POST)
            if data.is_valid():
                notes = request.POST['notes']
                code = request.session.get('document_code','0')
                document = Document.objects.get(code=code)
                document_notes = document.notes
                notes = notes + '\n' + name + '   ' + str(datetime.now()) + '\n'
                document_notes = document_notes + notes
                document.notes = document_notes   
                document.document_date = str(datetime.now())
                document.viewed = True
                document.save()
                return redirect(show_documents)
            else :
                error = data.errors
        return render(request,'documents/note.html',{'form':Send_notes,'error':error,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def send_notes(request):
    try :
        name = user_is_logined(request=request)
        error = ''
        task_name = 'add note'
        if request.method == "POST":
            data = Send_notes(request.POST)
            if data.is_valid():
                notes = request.POST['notes']
                code = request.session.get('document_code','0')
                document = Document.objects.get(code=code)
                document_notes = document.notes
                notes = notes + '\n' + name + '   ' + str(datetime.now()) + '\n'
                document_notes = document_notes + notes
                document.notes = document_notes   
                document.document_date = str(datetime.now())
                document.viewed = False
                document.save()
                messages.success(request, 'تم حفظ البيانات بنجاح!')
                return redirect(review_task)
            else :
                error = data.errors
        return render(request,'documents/note.html',{'form':Send_notes,'error':error,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def family_register(request):
    try :
        person = get_person(request=request)
        task_name = 'family register'
        event = False
        if person.status == 'single':
            national_num = person.national_dad
            person = get_by_obj(national_num=national_num)
        national_num = person.national_num
        family = get_family(national_num=national_num)
        request.session['task_name'] = task_name
        employee = request.session.get('employee','0')
        return render(request,'documents/confirm_family.html',{'person':person,'family':family,'task_name':task_name,'event':event,'employee':employee})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def birth_register(request):
    try :
        person = get_person(request=request)
        task_name = 'birth register'
        event = False
        request.session['task_name'] = task_name
        employee = request.session.get('employee','0')
        return render(request,'documents/confirm_person.html',{'person':person,'task_name':task_name,'event':event,'employee':employee})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def show_marriage_register(request):
    try :
        family = []
        person = get_person(request=request)
        national_num = request.GET.get('national_num')
        if national_num is not None :
            code = request.session.get('document_code','0')
            document = Document.objects.get(code=code)
            national_num = document.second_national_num
        partner_national_num = national_num
        partner = Person.objects.get(national_num=partner_national_num)
        if person.gender == 'male':
            husband = person
            wife = partner  
        else :
            husband = person
            wife = partner
        if partner in get_marrid(person):
            task_name = 'marriage'
            request.session['task_name'] = 'marriage register'
            event = Marrid.objects.get(national_wife=wife.national_num)
        if partner in get_divorce(person):
            task_name = 'divorce'
            divorce_times = Divorce.objects.filter(national_wife=wife.national_num)
            request.session['task_name'] = 'divorce register'
            for time in divorce_times :
                if time.national_hus == person.national_num :
                    event = time       
        family.append(husband)
        family.append(wife)
        request.session['second_national_num'] = wife.national_num
        employee = request.session.get('employee','0')
        return render(request,'documents/confirm_family.html',{'person':person,'family':family,'task_name':task_name,'event':event,'employee':employee})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def marriage_register(request):
    try :
        person = get_person(request=request)
        family = []
        if person.gender == 'male':
            task_name = 'all marriage'
        marrid_member = get_marrid(person)
        for user in marrid_member :
            family.append(user)
        if person.gender == 'female':
            task_name = 'marriage register'
        return render(request,'documents/show_all.html',{'person':person,'family':family,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')
    
def divorce_register(request):
    try :
        person = get_person(request=request)
        divorce_group = []
        if person.gender == 'male':
            task_name = 'divorce all'
        divorce_member = get_divorce(person)
        for user in divorce_member :
            divorce_group.append(user)
        if person.gender == 'female':
            task_name = 'divorce register'
        request.session['task_name'] = 'divorce register'
        return render(request,'documents/show_all.html',{'person':person,'family':divorce_group,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def dead_register_show(request):
    try :
        person = get_person(request=request)
        person_name =person.person_name
        task_name = 'dead register'
        code = request.session.get('document_code','0')
        document = Document.objects.get(code=code)
        national_dead = document.second_national_num
        if Dead.objects.filter(national_num=national_dead).exists():
            if Person.objects.filter(national_num=national_dead).exists():
                dead_person = Person.objects.get(national_num=national_dead)
                first_relation = get_first_relation(person)
                if dead_person in first_relation :
                    family =[]
                    family.append(dead_person)
                    event = Dead.objects.get(national_num=national_dead)
                    request.session['task_name'] = task_name
                    employee = request.session.get('employee','0')
                else :
                    error = "the person who asking can't see this dead person"
            else :
                error = "there's no one with this national number"
        else :
            error = "there's no one dead with this national number"
        return render(request,'documents/confirm_person.html',{'person':person,'task_name':task_name,'person_name':person_name,'error':error,'event':event,'employee':employee})         
    except:
        return HttpResponse('sorry there is an error please try another thing')

def dead_register(request):
    try :
        person = get_person(request=request)
        person_name =person.person_name
        error=' '
        task_name = 'dead register'
        if request.method == "POST":
            data = Dead_register(request.POST)
            if data.is_valid():
                national_dead = request.POST['national_dead']
                if Dead.objects.filter(national_num=national_dead).exists():
                    if Person.objects.filter(national_num=national_dead).exists():
                        dead_person = Person.objects.get(national_num=national_dead)
                        first_relation = get_first_relation(person)
                        if dead_person in first_relation :
                            family =[]
                            family.append(dead_person)
                            event = Dead.objects.get(national_num=national_dead)
                            request.session['task_name'] = task_name
                            employee = request.session.get('employee','0')
                            return render(request,'documents/confirm_person.html',{'person':person,'task_name':task_name,'person_name':person_name,'event':event,'employee':employee})
                        else :
                            error = "you can't see this dead person"
                    else :
                        error = "there's no one with this national number"
                else :
                    error = "there's no one dead with this national number"
        return render(request,'documents/note.html',{'form':Dead_register,'error':error,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def choose_document(request):
    try :
        task_name = 'choose document'
        documents = ['family register','birth register','marriage register','divorce register','dead register']
        return render(request,'documents/choose_document.html',{'documents':documents,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def get_document(request):
    try :
        if request.method == 'POST':
            name = request.POST.get('name')
            documents = {
                'family register' : 'family_register',
                'birth register' : 'birth_register',
                'marriage register' : 'marriage_register',
                'divorce register' : 'divorce_register',
                'dead register' : 'dead_register'
            }
            name = documents[name]
            url = f'{name}'
            return JsonResponse({'status': 'redirect', 'url': url})
        return JsonResponse({'status': 'fail'}, status=400)
    except:
        return HttpResponse('sorry there is an error please try another thing')

def review_task(request):
    try :
        code = request.GET.get('code')
        if  code == None :
            code = request.session.get('document_code','0')
        else :
            request.session['document_code'] = code
        document = Document.objects.get(code=code)
        task_name = document.name    
        employee = request.session.get('employee','0')
        return render(request,'documents/review_task.html',{'document':document,'task_name':task_name,'employee':employee}) 
    except:
        return HttpResponse('sorry there is an error please try another thing')

def show_documents(request):
    try :
        name = user_is_logined(request=request) 
        employee = request.session.get('employee','0')
        person = Person.objects.get(person_name=name)
        task_name = 'show documents'
        documents = []
        if employee == '0':
            documents = Document.objects.filter(person_national_num=person.national_num)
        else :
            documents = Document.objects.filter(viewed=False)
        return render(request,'documents/show_documents.html',{'documents':documents,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def show_new_documents(request):
    try :
        name = user_is_logined(request=request) 
        task_name = 'show documents'
        documents = []
        person_tasks = TaskPerson.objects.filter(person_name=name)
        for task in person_tasks:
            document = Document.objects.get(code=task.code)
            documents.append(document)
        return render(request,'documents/show_documents.html',{'documents':documents,'task_name':task_name})
    except:
        return HttpResponse('sorry there is an error please try another thing')

def delete_document(request):
    document_code = request.session.get('document_code','0')
    document = Document.objects.get(code=document_code)
    if TaskPerson.objects.filter(code=document_code).exists():
        TaskPerson.objects.get(code=document_code).delete()
    document.delete()
    try :
        del request.session['document_code']
    except:
        return HttpResponse('sorry there is an error please try another thing')
    return redirect(show_documents)

def insert_task(request):
    try :
        employee = request.session.get('employee','0')
        if employee =='0':
            last_document = Document.objects.order_by('code').last()
            if last_document:
                code = int(last_document.code) + 1
                code = str(code).zfill(8)
            name = user_is_logined(request=request) 
            task_name = request.session.get('task_name','0')
            person_national_num = Person.objects.get(person_name=name).national_num
            second_national_num =request.session.get('second_national_num',None)
            viewed = False
            notes = '  '
            document = Document(name=task_name,code=code,person_national_num=person_national_num,second_national_num=second_national_num,viewed=viewed,notes=notes)
            document.save()
            del request.session['task_name']
            request.session['second_national_num']='ads'
            del request.session['second_national_num']
        return redirect(main)
    except:
        return HttpResponse('sorry there is an error please try another thing')

def insert_task_code(request):
    last_document = Document.objects.order_by('code').last()
    if last_document:
        code = int(last_document.code) + 1
        code = str(code).zfill(8)
    person = get_person(request)
    task_name = request.session.get('task_name','0')
    person_national_num = person.national_num
    second_national_num =request.session.get('second_national_num',None)
    viewed = False
    notes = '  '
    document = Document(
        name=task_name,
        code=code,
        person_national_num=person_national_num,
        second_national_num=second_national_num,
        viewed=viewed,
        notes=notes
        )
    document.save()
    del request.session['task_name']
    request.session['second_national_num']='ads'
    del request.session['second_national_num']
    return code

def insert_document(request):
    try :
        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        document_name = document.name
        choices = {
            'family register':'family_register',
            'birth register':'birth_register',
            'marriage register':'show_marriage_register',
            'divorce register':'show_marriage_register',
            'dead register':'dead_register_show',
            'add information' : '../users/information_save',
            'add person':'../users/person_save',
            'add parent':'../users/parent_save',
            'add marrid' : '../users/add_marrid',
            'add divorce':'../users/add_divorce',
            'add widower':'../users/add_widower',
            'death record':'../users/death_save'
            }
        path = choices [document_name]
        url = path
        return redirect(url)
    except:
        return HttpResponse('sorry there is an error please try another thing')

