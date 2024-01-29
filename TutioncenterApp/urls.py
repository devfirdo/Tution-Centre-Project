from django.urls import path,include
from .import views  


urlpatterns = [
    path('',views.home,name='home'),
    path('Tsignup/',views.Tsignup,name='Tsignup'),
    path('login/',views.login,name='login'),
    path('Ssignup/',views.Ssignup,name='Ssignup'),
    path('main_login',views.main_login,name='main_login'),
    path('add_course',views.add_course,name='add_course'),
    path('tregistrations',views.tregistrations,name='tregistrations'),
    path('sregistrations',views.sregistrations,name='sregistrations'),
    path('reg_course',views.reg_course,name='reg_course'),
    path('approve_disapprove_users',views.approve_disapprove_users,name='approve_disapprove_users'),
    path('logout',views.logout,name='logout'),
    path('student_details',views.student_details,name='student_details'),
    path('delete_std/<int:pk>',views.delete_std,name='delete_std'),
    path('teacher_details',views.teacher_details,name='teacher_details'),
    path('delete_tcr/<int:pk>',views.delete_tcr,name='delete_tcr'),
    path('manage_course',views.manage_course,name='manage_course'),
    path('edit_course/<int:pk>',views.edit_course,name='edit_course'),
    path('update_course/<int:pk>',views.update_course,name='update_course'),
    path('tassign',views.tassign,name='tassign'),
    path('delete_course/<int:pk>',views.delete_course,name='delete_course'),
    path('assignment_form', views.assignment_form, name='assignment_form'),
    path('assign_teachers', views.assign_teachers, name='assign_teachers'),
    path('attandance_add', views.attandance_add, name='attandance_add'),
    path('add_teacher_attandance', views.add_teacher_attandance, name='add_teacher_attandance'),
    path('attandance_view', views.attandance_view, name='attandance_view'),
    path('view_teacher_attandance', views.view_teacher_attandance, name='view_teacher_attandance'),
    path('student_attendance', views.student_attendance, name='student_attendance'),
    path('view_student_attendance', views.view_student_attendance, name='view_student_attendance'),
    path('my_teacher_attendance',views.my_teacher_attendance,name = 'my_teacher_attendance'),
    path('view_assigned_students', views.view_assigned_students, name='view_assigned_students'),
    path('view_syll/', views.view_syll, name='view_syll'),
    path('view_course_syllabus/', views.view_course_syllabus, name='view_course_syllabus'),
    path('reset_passwords', views.reset_passwords, name='reset_passwords'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('view_coursesyllabus/', views.view_coursesyllabus, name='view_coursesyllabus'),
    path('student_password', views.student_password, name='student_password'),
    path('reset_password_student', views.reset_password_student, name='reset_password_student'),
    path('student_course_details', views.student_course_details, name='student_course_details'),
    path('individual_student_attendance', views.individual_student_attendance, name='individual_student_attendance'),
    path('student_profile', views.student_profile, name='student_profile'),
    path('edit_student_profile', views.edit_student_profile, name='edit_student_profile'),
    path('update_student_profile', views.update_student_profile, name='update_student_profile'),
    path('give_task', views.give_task, name='give_task'),
    path('view_submit_task', views.view_submit_task, name='view_submit_task'),
    path('view_assigned_students_tasks/', views.view_assigned_students_tasks, name='view_assigned_students_tasks'),
    path('view_submitted_pdf/<int:submission_id>/', views.view_submitted_pdf, name='view_submitted_pdf'),
    
    
    
   

    
]
