from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('professor-discipline-register/', views.availability, name='professor-discipline-register'),
    path('professor-courses/', views.professor_courses, name="professor-courses"),
    path('logout/', views.logout, name='logout'),
    path('student-courses/', views.student_courses, name='student-courses'),
    path('professor-disciplines', views.professor_disciplines, name='professor-disciplines'),
    #path('update-scheduled-time/', views.update_scheduled_time, name='update-scheduled-time'),
    path('student-disciplines/<course_id>', views.student_disciplines, name='student-disciplines'),
    path('all_availabilities/', views.all_availabilities, name='all_availabilities'), 
    path('add_availability/', views.add_availability, name='add_availability'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('profile/', views.profile, name="profile"),
    path('check-availability/<int:discipline_id>/<int:course_id>/', views.check_availability, name='check-availability'),
    path('send-availability-to-students/<int:discipline_id>', views.send_availability_to_students, name="send-availability-to-students"),
    path('get-username', views.get_username, name='get-username'),
    path('discipline-delete/<int:discipline_id>', views.discipline_delete, name='discipline-delete'),
    path('discipline-update-get/<int:discipline_id>', views.discipline_update_get, name='discipline-update-get'),
    path('discipline-post/<int:discipline_id>', views.discipline_update_post, name='discipline-update-post'),
    path('add-discipline', views.add_discipline, name='add-discipline'),
    path('course-update-get/<int:course_id>', views.course_update_get, name='course-update-get'),
    path('course-update-post/<int:course_id>', views.course_update_post, name='course-update-post'),
    path('course-delete/<int:course_id>', views.course_delete, name='course-delete'),
    path('add-course', views.add_course, name='add-course'),
    path('student-courses/', views.student_courses, name='student-courses'), #MUDAR NOME
    path('student-disciplines/', views.student_disciplines, name='student-disciplines'),
    path('availability/', views.availability, name='availability'),
    path('del_availability/', views.del_availability, name='del_availability'),
    path('courses-a/', views.courses_a, name='courses-a'), # curso para cadastrar a disponibilidade
    path('disciplines-a/', views.disciplines_a, name='disciplines-a'), # disciplina para cadastrar a disponibilidade
    path('professor-courses-card', views.professor_courses_card, name='professor-courses-card'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate-user'),
    path('save-scheduling/<time_id>/<status>/<subject>/', views.save_scheduling, name='save-scheduling'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('send_reset_password/', views.send_reset_password, name='send_reset_password'), #envia redefinição
    path('redefine_pass_user/<uidb64>/<token>', views.redefine_pass_user, name='redefine_pass_user'), #valida redefinição
    path('new_pass/<id_user>/<token>', views.new_pass, name='new_pass'), #validação 2 de token
]
