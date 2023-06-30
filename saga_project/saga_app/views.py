
from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Course, Discipline, Availability, Time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout as logout_django, login as login_django
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from django.shortcuts import redirect
from django.conf import settings
from rolepermissions.roles import assign_role
from .roles import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import date, datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from datetime import timedelta
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


    
def home(request):
   return render(request, 'home.html')

def login(request):
   if request.method == "GET":
    return render(request, 'login.html')
   else:
     email = request.POST.get('email')
     password = request.POST.get('password')

     user = authenticate(request, email=email, password=password)
     
     if user:
      login_django(request, user)
      if request.user.is_authenticated:
        return redirect('home')
     else:
      return HttpResponse("Usuário ou senha inválidos")
     
def logout(request):
  logout_django(request)
  return render(request, 'login.html')

'''@login_required(login_url="/")
def plataform(request):
    if request.user.is_authenticated:
      return render(request, 'courses.html')'''
    
def sign_up(request):
   if request.method == "GET":
    return render(request, 'cadastro.html')
   else:
      first_name = request.POST.get('first-name')
      last_name = request.POST.get('last-name')
      email = request.POST.get('email')
      password = request.POST.get('password')
      password1 = request.POST.get('password-confirm')
      phone = request.POST.get('phone')
      user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, phone=phone)
      user.save()
      assign_role(user, "student")
      messages.success(request, "Usuário cadastrado com sucesso!")
      return render(request, "login.html")
    

#@has_role_decorator('professor')
def discipline_register(request):
    if request.method == "GET":
      courses = Course.objects.all()
      return render(request, 'discipline-register.html', {"courses": courses})
    else:
      '''discipline_name = request.POST.get('discipline-name')
      access_key = request.POST.get('access-key')
      year = request.POST.get('year')
      semester = request.POST.get('semester')
      discipline = Discipline(name=discipline_name, access_key=access_key,semester=semester)
      discipline.save()
      courses_ids = request.POST.getlist('boxes') 
      for i in range(len(courses_ids)):
        courses_ids[i] = Course.objects.get(id=courses_ids[i])
        discipline.courses.add(courses_ids[i])
      discipline.save()
      messages.success(request, "Disciplina cadastrada com sucesso!")'''
      return redirect('discipline-register')

@login_required(login_url="/")
def student_courses(request):
  if request.method == "GET":
    courses = Course.objects.all() 
    paginator = Paginator(courses, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "student-courses.html", {"courses": page_obj})
  
@login_required(login_url="/")
def disciplines_a(request):
  if request.method == "GET":
    return render(request, "courses-a.html")
  else:
    id_course = request.POST.get('course-id')
    course = Course.objects.get(id=id_course)
    disciplines = course.disciplines.all()
    return render(request, "disciplines-a.html", {"disciplines": disciplines, "course":course}) # passa nome do curso

@login_required(login_url="/")
def courses_a(request):
  if request.method == "GET":
    courses = Course.objects.all() 
    paginator = Paginator(courses, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "courses-a.html", {"courses": page_obj})
       

@login_required(login_url="/")
def student_disciplines(request):
  if request.method == "GET":
    return render(request, "student-courses.html")
  else:
    id_course = request.POST.get('course-id')
    course = Course.objects.get(id=id_course)
    disciplines = course.disciplines.all()
    return render(request, "student-disciplines.html", {"disciplines": disciplines, "course":course}) # passa nome do curso  


@login_required(login_url="/")
def student_disciplines(request, course_id):
  if request.method == "POST":
    course = Course.objects.get(id=course_id)
    disciplines = Discipline.objects.filter(courses=course)
    return render(request, "student-disciplines.html", {"disciplines": disciplines})

@login_required(login_url="/") 
def professor_disciplines(request):
  disciplines = Discipline.objects.all()
  return render(request, "professor-disciplines.html", {"disciplines": disciplines})

def add_discipline(request):
    if request.method == "GET":
      courses = Course.objects.all()
      return render(request, 'add-discipline.html', {"courses": courses})
    else:
      discipline_name = request.POST.get('discipline-name')
      access_key = request.POST.get('access-key')
      semester = request.POST.get('semester')
      professor = request.user
      discipline = Discipline(name=discipline_name, access_key=access_key,semester=semester)
      discipline.save()
      discipline.professor.add(professor)
      discipline.save()
      courses_ids = request.POST.getlist('boxes')
      for i in range(len(courses_ids)):
        courses_ids[i] = Course.objects.get(id=courses_ids[i])
        discipline.courses.add(courses_ids[i])
      discipline.save()
      messages.success(request, "Disciplina cadastrada com sucesso!")
      return redirect('add-discipline')

@require_http_methods(["POST"]) 
def discipline_delete(request, discipline_id):
    discipline = Discipline.objects.get(id=discipline_id)
    discipline.delete()
    messages.success(request, 'Disciplina excluída com sucesso!')
    return redirect('professor-disciplines')


def discipline_update_get(request, discipline_id):
  discipline = Discipline.objects.get(id=discipline_id)
  courses = Course.objects.all()
  discipline_courses = Discipline.objects.values_list('courses__id', flat=True)
  if request.method == "GET":
    return render(request, 'discipline-update.html', {'discipline': discipline, 'courses': courses, 'discipline_courses': discipline_courses})

@require_http_methods(["POST"])
def discipline_update_post(request, discipline_id):
  discipline = Discipline.objects.get(id=discipline_id)
  discipline.name = request.POST.get('discipline-name')
  discipline.access_key = request.POST.get('access-key')
  discipline.semester = request.POST.get('semester')
  discipline.courses.set(request.POST.getlist('boxes'))
  discipline.save()
  messages.success(request, "Disciplina atualizada com sucesso!")
  return redirect('discipline-update-get', discipline_id=discipline_id)

def add_course(request):
  if request.method == "GET":
    return render(request, 'add-course.html')
  else:
    course_name = request.POST.get('course-name')
    course = Course(name=course_name)
    course.save()
    messages.success(request, 'Curso cadastrado com sucesso!')
    return redirect('add-course')

def course_update_get(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == "GET":
      return render(request, 'course-update.html', {'course': course})

@require_http_methods(["POST"]) 
def course_update_post(request, course_id):
  course = Course.objects.get(id=course_id)
  course.name = request.POST.get('course-name')
  course.save()
  return redirect('professor-courses')

@require_http_methods(["POST"]) 
def course_delete(request, course_id):
  course = Course.objects.get(id=course_id)
  course.delete()
  messages.success(request, 'Curso excluído com sucesso!')
  return redirect('professor-courses')

@login_required(login_url="/")
def student_courses(request):
  if request.method == "GET":
    courses = Course.objects.all()
    paginator = Paginator(courses, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "student-courses.html", {"courses": page_obj})


#@has_role_decorator('professor')
def professor_courses(request):
  if request.method == "GET":
    courses = Course.objects.all()
    return render(request, 'professor-courses.html', {"courses": courses})
  


@login_required(login_url="/")
def profile(request):
  if request.method == "GET":
    return render(request, 'profile.html')
  else:
    first_name = request.POST.get('first-name')
    last_name = request.POST.get('last-name')
    email = request.POST.get('email')
    '''password = request.POST.get('password')
    password1 = request.POST.get('password-confirm')'''
    phone = request.POST.get('phone')
    profile_picture = request.FILES['profile-picture']
    uploaded_file = SimpleUploadedFile(profile_picture.name, profile_picture.read(), content_type=profile_picture.content_type)
    user_update = User.objects.get(email=email)
    user_update.first_name = first_name
    user_update.last_name = last_name
    user_update.phone = phone
    user_update.profile_image.save(profile_picture.name, uploaded_file, save=True)
    user_update.save()
    return redirect('profile')


  


def all_availabilities(request):
  all_availabilities = Availability.objects.all()
  out = []
  for availability in all_availabilities:
    out.append({
      'title': availability.name,
      'id': availability.id,
      'start': availability.start.strftime("%d/%m/%Y, %H:%M:%S"),
      'end': availability.end.strftime("%d/%m/%Y, %H:%M:%S")
    })
    return JsonResponse(out, safe=False)

@has_role_decorator("professor")
def add_availability(request):
  start = request.GET.get("start", None)
  end = request.GET.get("end", None)
  title = request.GET.get("title", None)
  availability = Availability(name=str(title), start=start, end=end)
  availability.save()
  data = {}
  return JsonResponse(data)

def update(request):
  start = request.GET.get("start", None)
  end = request.GET.get("end", None)
  title = request.GET.get("title", None)
  id = request.GET.get("id", None)
  availability = Availability.objects.get(id=id)
  availability.start = start
  availability.end = end
  availability.name = title
  availability.save()
  data = {}
  return JsonResponse(data)

def remove(request):
  id = request.GET.get("id", None)
  availability = Availability.objects.get(id=id)
  availability.delete()
  data = {}
  return JsonResponse(data)

'''def availability(request):
    if request.method == "GET":
      return render(request, 'availability.html')
    else:
      initial_datetime = request.POST.get("initial-datetime")
      final_datetime = request.POST.get("final-datetime")
      duration = int(request.POST.get("duration"))
      
      av1 = Availability.objects.filter(initial_datetime=initial_datetime).first()
      av2 = Availability.objects.filter(final_datetime=final_datetime).first()
      
      if av1 and av2:
        return HttpResponse("Já existe disponibilidade cadastrada para o mesmo horário")
      if int(initial_datetime[8:10]) < int(str(datetime.date.today())[8:10]):
        return HttpResponse("Data inicial não pode ser anterior à data atual")
      availability = Availability(initial_datetime=initial_datetime, final_datetime=final_datetime, duration=duration)
      availability.save()
      dia_semana = request.POST.getlist("dia-semana")
      gerar_horario(availability,dia_semana)

def gerar_horario(availability:Availability,dia_semana):
    data_inicio = datetime.date(availability.initial_datetime[0:4], availability.initial_datetime[5:7], availability.initial_datetime[8:10]) 
    data_fim = datetime.date(availability.final_datetime[0:4], availability.final_datetime[5:7], availability.final_datetime[8:10]) 
    hora_inicial = datetime.time(availability.initial_datetime[11:13], availability.initial_datetime[14:16], availability.initial_datetime[17:19]) 
    hora_final = datetime.time(availability.final_datetime[11:13], availability.final_datetime[14:16], availability.final_datetime[17:19]) 

    data_teste = data_inicio
    while (data_teste <= data_fim):     
      if Time.objects.filter(date=data_teste,initial_time__ge=datetime.time(hora_inicial),final_time__le=datetime.time(hora_inicial)).first(): # ferifica se a hora_inicial a ser cadastrada está entre um registro da tabela
        return HttpResponse("Hora inicial em conflito com registros existentes") #renderizar erro
      elif Time.objects.filter(date=data_teste,initial_time__ge=datetime.time(hora_final),final_time__le=datetime.time(hora_final)).first(): #ferifica se a hora_final a ser cadastrada está entre um registro da tabela
        return HttpResponse("Hora Final em conflito com registros existentes") #renderizar erro
      else: #cadsatrar os horarios na tabela com suas respectivas divisões
        for i in dia_semana:  #percorre os indices da semana
          if data_teste.weekday() == i: #verifica se a data é do dia da semana correspondete
            #dividir horario e incluir na tabela TIME
            pass

      data_teste = data_teste + datetime.timedelta(days=1) 
      return HttpResponse("Registros incluidos com sucesso")'''


def gerar_horario(availability:Availability,dia_semana,usuario_logado:User, disciplina:Discipline):
    data_inicio = availability.initial_datetime.date()
    data_fim = availability.final_datetime.date() 
    hora_inicial = availability.initial_datetime.time()
    hora_final = availability.final_datetime.time()
    data_teste = data_inicio
  

    while data_teste <= data_fim:
      if Time.objects.filter(date=data_teste,initial_time__range=(hora_inicial, hora_final), final_time__range=(hora_inicial, hora_final), professor=usuario_logado).first(): # verifica se a hora_inicial a ser cadastrada está entre um registro da tabela
        retorno = False
        return retorno   
      else: #cadsatrar os horarios na tabela com suas respectivas divisões
        for i in dia_semana:  #percorre os indices da semana
          if data_teste.weekday() == i: #verifica se a data é do dia da semana correspondete
            datetime_ini = datetime.combine(data_teste, hora_inicial) #junta hora e data
            datetime_fin = datetime.combine(data_teste, hora_final) #junta hora e data
            while datetime_ini < datetime_fin: #teste se a hora iniciar ainda é menor que a final
              datetime_ini_ant = datetime_ini #salva a hora antes do encremento 
              datetime_ini += timedelta(minutes=availability.duration) #encrementa a hora 
              if datetime_ini <= datetime_fin:
                new_time = Time(date=data_teste, initial_time=datetime_ini_ant.time(), final_time=datetime_ini.time(), status=False, subject="Livre", professor=usuario_logado, discipline=disciplina)       #cria o registro     
                new_time.save()
      data_teste = data_teste + timedelta(days=1)
      retorno = True
    return retorno
    

def del_availability(request):
  if request.method == "GET":
      disc = Availability.objects.all()
      return render(request, 'Availability.html', {"availability": disc})
  else:
    id_availability = request.POST.get('availability-id')
    availability = Availability.objects.get(id=id_availability)
    return_del_time = excluir_horario(availability)
    if return_del_time == True:
      availability.delete()
      return HttpResponse("Resitros de Disponibilidade excluido com sucesso")
    else:
      return HttpResponse("Não foi possivel excluir a disponibilidade!!! Nao foi encontrado registros de horarios maiores que a data atual para a disponibilidade a ser excluida!")

def excluir_horario(availability:Availability):
    data_inicio = availability.initial_datetime.date()
    data_fim = availability.final_datetime.date() 
    hora_inicial = availability.initial_datetime.time()
    hora_final = availability.final_datetime.time()
    data_teste = data_inicio
    cont = 0
    retorno = False
    while data_teste <= data_fim:
      if data_teste > date.today():
        if Time.objects.filter(date=data_teste,initial_time__range=(hora_inicial, hora_final), final_time__range=(hora_inicial, hora_final), discipline=availability.discipline, professor=availability.professor).delete(): # ferifica se a hora_inicial a ser cadastrada está entre um registro da tabela
          cont += 1
      data_teste = data_teste + timedelta(days=1)
    if cont > 0:
      retorno = True 
    return retorno

def check_availability(request, discipline_id):
    professor = int(request.POST.get('professor'))
    if professor == 0:
      discipline = Discipline.objects.get(id=discipline_id)
      return render(request, 'check-availability.html', {'id': request.user.id, 'first_name': request.user.first_name + " " + request.user.last_name, 'discipline': discipline})
    elif professor == 1:
       discipline = Discipline.objects.get(id=discipline_id)
       return render(request, 'check-availability-professor.html', {'id': request.user.id, 'first_name': request.user.first_name + " " + request.user.last_name, 'discipline': discipline})

def professor_courses_card(request):
  if request.method == "GET":
    courses = Course.objects.all() 
    paginator = Paginator(courses, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "professor-courses-card.html", {"courses": page_obj})

def send_availability_to_students(request, discipline_id):
  data = Time.objects.filter(discipline_id=discipline_id).values()
  if not request.user.professor:
    return JsonResponse(list(data), safe=False)
  else:
    updated_data = []
    # Obtendo os nomes dos estudantes correspondentes aos student_id
    for item in data:
        if item['student_id'] != None:
          student_id = item['student_id']
          student = get_object_or_404(User, id=student_id)  
          item['student_id'] = f'{student.first_name} {student.last_name}' # Atualizando o valor com o nome do estudante
          updated_data.append(item)
        else:
          updated_data.append(item)
    return JsonResponse(updated_data, safe=False)



def get_username(request):
  print(request.user.first_name)
  if request.user.is_authenticated:
        username = request.user.first_name
        return JsonResponse({'username': username})
  else:
      return JsonResponse({'username': None})
  
def get_user(user):
  if user.is_authenticated:
        username = user
        return username


def availability(request):
    if request.method == "GET": #se o usuario tentar acessar direto a pagina será direcionado a escolha do curso
      courses = Course.objects.all()
      paginator = Paginator(courses, 8)
      page_number = request.GET.get('page')
      page_obj = paginator.get_page(page_number)
      return render(request, "courses-a.html", {"courses": page_obj})
    
    elif request.POST.get("register_availability") == "0": # verifica se está vindo da pagina com a info de disciplina e sem o cadastro da disponivilide
      disciplina = Discipline.objects.filter(id=request.POST.get("disciplina_id")).first() #Pega disciplina
      usuario_logado = get_user(request.user)
      disc = Availability.objects.filter(professor=usuario_logado, discipline=disciplina) #Filtrar disponibilidade e discliplina selecionada do professor logado.
      return render(request, 'availability.html', {"availability": disc, "discipline":disciplina})
    
    elif request.POST.get("register_availability") == "1": # verifica se vem do formulario de registro da disponibilidade
      initial_datetime = request.POST.get("initial-datetime")
      initial_datetime = datetime.strptime(initial_datetime[0:4] + "/" + initial_datetime[5:7] + "/" + initial_datetime[8:10] + " " + initial_datetime[11:13] + ":" + initial_datetime[14:16]  ,"%Y/%m/%d %H:%M")
      
      final_datetime = request.POST.get("final-datetime")
      final_datetime = datetime.strptime(final_datetime[0:4] + "/" + final_datetime[5:7] + "/" + final_datetime[8:10] + " " + final_datetime[11:13] + ":" + final_datetime[14:16]  ,"%Y/%m/%d %H:%M")
      duration = int(request.POST.get("duration"))
      
      usuario_logado = get_user(request.user)
      disciplina = Discipline.objects.filter(id=request.POST.get("disciplina_id")).first() #Pega disciplina
      av1 = Availability.objects.filter(initial_datetime=initial_datetime, professor=usuario_logado, discipline=disciplina).first()
      av2 = Availability.objects.filter(final_datetime=final_datetime, professor=usuario_logado, discipline=disciplina).first()
      
      if av1 and av2:
        return HttpResponse("Já existe disponibilidade cadastrada para o mesmo horário")
      availability = Availability(initial_datetime=initial_datetime, final_datetime=final_datetime, duration=duration, professor=usuario_logado, discipline=disciplina)
      dia_semana =  request.POST.getlist("selected-days")
      dia_semana = [int(dia) for dia in dia_semana] #transforma em lista de inteiros
      print(dia_semana)
      return_time = gerar_horario(availability,dia_semana,usuario_logado,disciplina) #passar professor
      if return_time == True:
        availability.save()
        #Colocar mensagem
        '''return redirect('availability', disciplina.id)'''
        disc = Availability.objects.filter(professor=usuario_logado, discipline=disciplina)
        return render(request, 'availability.html', {"availability": disc, "discipline":disciplina})
      if return_time == False:
        return HttpResponse("Não foi possivel criar registros no tabela Time, Verifique conflitos de agenda")


@csrf_exempt
def update_scheduled_time(request):
    if request.method == 'POST':
        scheduled = False if (request.POST.get('scheduled')) == 'false' else True
        schedule_id = int(request.POST.get('schedule_id'))
        student_id = int(request.POST.get('student_id'))
        student = User.objects.get(id=student_id)
        time = Time.objects.get(id=schedule_id)
        
        if scheduled == False:
          time.status = False
          time.student = None
        else:
          time.status = True
          time.student = student

        time.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})



def professor_register(request):
  if request.method == "GET":
    return render(request, 'professor-register.html')
  

      

  

      
      
       