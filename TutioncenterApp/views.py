from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import auth
from TutioncenterApp.models import CustomUser,Assignment,Teacherattendance,StudentAttendance
from TutioncenterApp.models import Usermembers
from TutioncenterApp.models import Courses,Task, TaskSubmission
from django.contrib import messages
import random
import re
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.http import FileResponse, Http404
import os
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



def home(request):
    return render(request,'home.html')  
def Tsignup(request):
    crs = Courses.objects.all()
    return render(request,'Tsignup.html',{'crs':crs})

def Ssignup(request):
    crs = Courses.objects.all()
    return render(request,'Ssignup.html',{'crs':crs})   

def login(request):
    return render(request,'login.html')

def sregistrations(request):
    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        usename = request.POST.get('uname')
        age = request.POST.get('age')
        number = request.POST.get('num')
        email = request.POST.get('mail')
        image = request.FILES.get('image')
        txt = request.POST.get('text')
        password = str(random.randint(100000,999999))
        sel = request.POST.get('sel')
        coursename = Courses.objects.get(id=sel)
        if CustomUser.objects.filter(username=usename) or CustomUser.objects.filter(email=email).exists():
            messages.error(request,'user already exists')
            return render(request,'Ssignup.html')
        else:
            user = CustomUser.objects.create_user(username=usename,password=password,email=email,first_name=firstname,last_name=lastname,user_type=txt,is_active=False)
            user.save()
            std = Usermembers(user_course = coursename,age =age,number =number,image=image,user_member=user)
            std.save()
            subject = 'Registration Confirmation'
            message = 'registration successfull ,wait for admin approval'
            send_mail(subject,"Hello " + usename +' '+ message ,settings.EMAIL_HOST_USER,{email})
            messages.success(request, 'User registration successful. Please wait for admin approval.')
            return render(request, 'Ssignup.html')


def tregistrations(request):
    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        usename = request.POST.get('uname')
        age = request.POST.get('age')
        number = request.POST.get('num')
        email = request.POST.get('mail')
        image = request.FILES.get('image')
        txt = request.POST.get('text')
        password = str(random.randint(100000,999999))
        sel = request.POST.get('sel')
        coursename = Courses.objects.get(id=sel)
        if CustomUser.objects.filter(username=usename).exists() or CustomUser.objects.filter(email=email).exists():
            messages.error(request,'user already exists')
            return render(request,'Tsignup.html')
        else:
            user = CustomUser.objects.create_user(username=usename,password=password,email=email,first_name=firstname,last_name=lastname,user_type=txt,is_active=False)
            user.save()
            tcr = Usermembers(user_course = coursename,age =age,number =number,image=image,user_member=user)
            tcr.save()
            subject = 'Registration Confirmation'
            message = 'registration successfull ,wait for admin approval'
            send_mail(subject,"Hello " + usename +' '+ message ,settings.EMAIL_HOST_USER,{email})
            messages.success(request, 'User registration successful. Please wait for admin approval.')
            return render(request, 'Tsignup.html') 

def main_login(request):
    if request.method == 'POST':
        pending_users = CustomUser.objects.filter(is_active=False)
        pending_count = pending_users.count()
        username = request.POST.get('uname')
        password = request.POST.get('upass')
        usr = auth.authenticate(request, username=username, password=password)
        if usr is not None:
            if usr.is_superuser:
                auth.login(request, usr)
                return render(request,'admin/admin_home.html',{'pending_count': pending_count})
            elif usr.user_type == '3':
                auth.login(request, usr)
                usr = Usermembers.objects.get(user_member=request.user)
                return render(request,'student/student_home.html',{'usr':usr})
            else:
                auth.login(request, usr)
                
                current_teacher = request.user.id
                usr = Usermembers.objects.get(user_member=request.user)
                tcr = CustomUser.objects.get(id=current_teacher)
                return render(request,'teacher/teacher_home.html',{'tcr':tcr,'usr':usr})
        else:
            messages.error(request,'invalid credentials')
            return render(request,'login.html')
@login_required     
def add_course(request):
    pending_users = CustomUser.objects.filter(is_active=False)
    pending_count = pending_users.count()
    return render(request,'admin/add_course.html',{'pending_count': pending_count})


@login_required    
def reg_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('acourse')
        syllabus = request.FILES.get('syllabus')
        course_fee = request.POST.get('acoursefee')
        course_duration = request.POST.get('sel')
        course = Courses(course_name=course_name,syllabus=syllabus,course_fee=course_fee,course_duration=course_duration)
        course.save()
        messages.success(request,'course added successfully')
        return render(request,'admin/add_course.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


@login_required
def approve_disapprove_users(request):
    pending_users = CustomUser.objects.filter(is_active=False)
    approved_users = CustomUser.objects.filter(is_active=True)
    pending_count = pending_users.count()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(CustomUser, id=user_id)

        if action == 'approve': 
            password = str(random.randint(100000, 999999))
            user.set_password(password)
            user.is_active = True
            user.save()

            subject = 'Registration Approved'
            message = f"Hello {user.username}, your username is {user.username} and your password is {password}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Approved')
            return redirect('approve_disapprove_users')

        elif action == 'disapprove':
            user.delete()
            return redirect('approve_disapprove_users')

    return render(request, 'admin/approve.html', {'pending_users': pending_users, 'pending_count': pending_count, 'approved_users': approved_users})

@login_required
def student_details(request):
    std = Usermembers.objects.all()
    return render(request, 'admin/studentrecord.html',{'std': std})
@login_required
def delete_std(request,pk):
    std = Usermembers.objects.get(id=pk)
    crs = CustomUser.objects.get(username=std.user_member.username)
    std.delete()
    crs.delete()
    return redirect('student_details')
@login_required
def teacher_details(request):
    tcr = Usermembers.objects.all()
    return render(request, 'admin/teacherrecord.html',{'tcr': tcr})
@login_required
def delete_tcr(request,pk):
    tcr = Usermembers.objects.get(id=pk)
    crs = CustomUser.objects.get(username=tcr.user_member.username)
    tcr.delete()
    crs.delete()
    return redirect('teacher_details')
@login_required
def manage_course(request):
    crs = Courses.objects.all()
    return render(request, 'admin/managecourse.html',{'crs': crs})
@login_required
def delete_course(request,pk):
    crs = Courses.objects.get(id=pk)
    users = Usermembers.objects.filter(user_course=crs)
    users.delete()
    crs.delete()
    return redirect('manage_course')
@login_required
def edit_course(request, pk):
    crs = Courses.objects.get(id=pk)
    all_durations = Courses.objects.all()
    return render(request, 'admin/editcourse.html', {'crs': crs, 'all_durations': all_durations})
@login_required
def update_course(request, pk):
    if request.method == 'POST':
        crs = Courses.objects.get(id=pk)
        crs.course_name = request.POST.get('nme')
        crs.course_fee = request.POST.get('fee')
        crs.course_duration = request.POST.get('duration')
        crs.syllabus = request.FILES.get('syllabus_pdf')
        crs.save()

        return redirect('manage_course') 

    return render(request, 'admin/editcourse.html')

@login_required
def tassign(request):
    crs = Courses.objects.all()
    memb = Usermembers.objects.all()
    return render(request, 'admin/tassign.html', {'crs': crs,'memb': memb})

@login_required
def assignment_form(request):
    courses = Courses.objects.all()
    usr = Usermembers.objects.all()
    students = Usermembers.objects.filter(user_member__user_type=3)
    teachers = Usermembers.objects.filter(user_member__user_type=2)

    context = {
        'crs': courses,
        'tcr': teachers,
        'std': students,
        'usr': usr,
    }

    return render(request, 'admin/assigned.html', context)
@login_required
def assign_teachers(request):
    if request.method == 'POST':
        course_id, student_id = request.POST.get('assign').split('_')
        teacher_id = request.POST.get(f'teacher_name_{course_id}_{student_id}')

        course = Courses.objects.get(id=course_id)
        student = Usermembers.objects.get(id=student_id)
        teacher = CustomUser.objects.get(id=teacher_id)

        existing_assignment = Assignment.objects.filter(user_member=student, course=course).first()

        if existing_assignment:
            existing_assignment.user_teacher = teacher
            existing_assignment.save()
        else:
            assignment = Assignment(user_member=student, user_teacher=teacher, course=course)
            assignment.save()

    return redirect('assignment_form')


@login_required
def attandance_add(request):
    teacher = Usermembers.objects.filter(user_member__user_type=2)
    return render(request, 'admin/attendance_form.html', {'teachers': teacher})

@login_required
def add_teacher_attandance(request):
    if request.method == 'POST':
        sel = request.POST['sel']
        teacher_member = Usermembers.objects.get(id=sel, user_member__user_type='2')
        teacher = teacher_member.user_member 
        date = request.POST['date']
        attendance = request.POST.get('attendance')
        attandancetable = Teacherattendance(teacher_name=teacher, date=date, attendance=attendance)
        attandancetable.save()
        messages.success(request,'Attendance added successfully')
        return redirect('attandance_add')


@login_required
def attandance_view(request):
    teacher = Usermembers.objects.filter(user_member__user_type='2')
    return render(request, 'admin/attendance_report.html', {'teachers': teacher})

@login_required
def view_teacher_attandance(request):
    print("View function triggered")

    if request.method == 'POST':
        sel = request.POST['sel']
        teacher_member = Usermembers.objects.get(id=sel, user_member__user_type=2)
        teacher = teacher_member.user_member  
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        attandance_records = Teacherattendance.objects.filter(teacher_name=teacher, date__range=[startdate, enddate])
        return render(request, 'admin/viewattendance.html', {'teacher': teacher, 'atr': attandance_records})
    

@login_required
def student_attendance(request):
    current_teacher = request.user.id
    assignments = Assignment.objects.filter(user_teacher=current_teacher)
    students_assigned = Usermembers.objects.filter(id__in=assignments.values_list('user_member', flat=True))
    
    if request.method == 'POST':
        selected_student_id = request.POST.get('sel')
        date = request.POST.get('date')
        attendance_status = request.POST.get('attendance')

        student = Usermembers.objects.get(id=selected_student_id)
        attendance_record = StudentAttendance(student_name=student, date=date, attendance=attendance_status)
        attendance_record.save()
        messages.success(request,'Attendance record updated successfully')

    return render(request, 'teacher/student_attendance.html', {'students_assigned': students_assigned})


@login_required
def view_student_attendance(request):
    current_teacher = request.user.id
    assignments = Assignment.objects.filter(user_teacher=current_teacher)
    students_assigned = Usermembers.objects.filter(id__in=assignments.values_list('user_member', flat=True))

    if request.method == 'POST':
        selected_student_id = request.POST.get('sel')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        student = Usermembers.objects.get(id=selected_student_id)
        attendance_records = StudentAttendance.objects.filter(student_name=student, date__range=[start_date, end_date])

        return render(request, 'teacher/view_student_attendance.html', {'students_assigned': students_assigned, 'attendance_records': attendance_records})

    return render(request, 'teacher/view_student_attendance.html', {'students_assigned': students_assigned})



@login_required
def my_teacher_attendance(request):
    current_teacher = request.user
    teacher_attendance = Teacherattendance.objects.filter(teacher_name=current_teacher)
    
    return render(request, 'teacher/view_teacher_attendance.html', {'teacher_attendance': teacher_attendance})


@login_required
def view_assigned_students(request):
    current_teacher = request.user
    assigned_students = Assignment.objects.filter(user_teacher=current_teacher)

    return render(request, 'teacher/view_assigned_students.html', {'assigned_students': assigned_students})


@login_required
def view_syll(request):
    return render(request, 'teacher/view_course_syllabus.html')


@login_required
def view_course_syllabus(request):
    current_teacher = request.user
    assigned_courses = Assignment.objects.filter(user_teacher=current_teacher)
    
    return render(request, 'teacher/view_course_syllabus.html', {'assigned_courses': assigned_courses})


@login_required
def reset_passwords(request):
    current_teacher = request.user
    password = CustomUser.objects.get(username = current_teacher)
    return render(request, 'teacher/reset_passwords.html', {'password': password})


@login_required
def reset_password(request):
    if request.method == 'POST':
        current_password = request.POST['current']
        new_password = request.POST['passwd']
        confirm_password = request.POST['cpasswd']

        current_teacher = request.user
        user = CustomUser.objects.get(username=current_teacher)
        
        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect!')
            return redirect('reset_password')


        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long!')
            return redirect('reset_password')

        if not re.search(r'\d', new_password):
            messages.error(request, 'Password must contain at least one number!')
            return redirect('reset_password')

        if not re.search(r'[A-Z]', new_password):
            messages.error(request, 'Password must contain at least one capital letter!')
            return redirect('reset_password')

        if new_password == confirm_password:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
    return render(request, 'teacher/reset_passwords.html')


@login_required
def view_coursesyllabus(request):
    current_student = Usermembers.objects.get(user_member=request.user)
    assigned_courses = Assignment.objects.filter(user_member=current_student)

    return render(request, 'student/course_syllabus.html', {'assigned_courses': assigned_courses})


@login_required
def student_password(request):
    return render(request, 'student/reset_passwords.html')


@login_required
def reset_password_student(request):
    if request.method == 'POST':
        current_password = request.POST['current']
        new_password = request.POST['passwd']
        confirm_password = request.POST['cpasswd']

        current_user = request.user
        user = CustomUser.objects.get(username=current_user)

        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect!')
            return redirect('reset_password_student')

        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long!')
            return redirect('reset_password_student')

        if not re.search(r'\d', new_password):
            messages.error(request, 'Password must contain at least one number!')
            return redirect('reset_password_student')

        if not re.search(r'[A-Z]', new_password):
            messages.error(request, 'Password must contain at least one capital letter!')
            return redirect('reset_password_student')

        if new_password == confirm_password:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
    return render(request, 'student/reset_passwords.html')


@login_required
def student_course_details(request):
    current_student = Usermembers.objects.get(user_member=request.user)
    assigned_courses = Assignment.objects.filter(user_member=current_student)
    return render(request,'student/view_course.html', {'assigned_courses': assigned_courses})


@login_required
def individual_student_attendance(request):
    current_student = Usermembers.objects.get(user_member=request.user)
    attendance_records = StudentAttendance.objects.filter(student_name=current_student)

    return render(request, 'student/view_attendance.html', {
        'attendance_records': attendance_records,
    })


@login_required
def student_profile(request):
    current_student = Usermembers.objects.get(user_member=request.user)
    return render(request,'student/student_profile.html', {
        'current_student': current_student,
    })


@login_required
def edit_student_profile(request):
    current_student = Usermembers.objects.get(user_member=request.user)
    return render(request,'student/edit_profile.html', {'current_student': current_student})


@login_required
def update_student_profile(request):
    if request.method == 'POST':
        current_student = Usermembers.objects.get(user_member=request.user)
        current_student.user_member.first_name = request.POST.get('fname')
        current_student.user_member.last_name = request.POST.get('lname')
        current_student.user_member.email = request.POST.get('mail')
        current_student.number = request.POST.get('num')
        current_student.age = request.POST.get('age')

        if request.FILES.get('img'):
            current_student.image = request.FILES['img']

        current_student.user_member.save()
        current_student.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('student_profile')

    return render(request, 'student/edit_profile.html', {'current_student': current_student})


@login_required
def give_task(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        task = Task.objects.create(task_name=task_name, start_date=start_date, end_date=end_date)

        assigned_students_ids = request.POST.getlist('assigned_students')
        for student_id in assigned_students_ids:
            student = Usermembers.objects.get(id=student_id)
            TaskSubmission.objects.create(task=task, user_member=student)

        messages.success(request, 'Task assigned successfully!')
        return redirect('give_task')

    assigned_students = Usermembers.objects.filter(assignment__user_teacher=request.user).distinct()
    context = {'assigned_students': assigned_students}
    return render(request, 'teacher/give_task.html', context)


@login_required
def view_submit_task(request):
    current_student = Usermembers.objects.get(user_member=request.user)
    task_submissions = TaskSubmission.objects.filter(user_member=current_student)

    if request.method == 'POST':
        submitted_task_file = request.FILES.get('submitted_task_file')

        if submitted_task_file:
            task_id = request.POST.get('task_id')
            task = Task.objects.get(pk=task_id)

            existing_submission = TaskSubmission.objects.filter(user_member=current_student, task=task).first()

            if existing_submission:
                existing_submission.submitted_task_file = submitted_task_file
                existing_submission.save()
            else:
                TaskSubmission.objects.create(
                    task=task,
                    user_member=current_student,
                    submitted_task_file=submitted_task_file
                )

            messages.success(request, 'Task submitted successfully!')
            return redirect('view_submit_task')

    tasks_to_display = Task.objects.filter(tasksubmission__user_member=current_student).distinct()

    context = {'task_submissions': task_submissions, 'tasks_to_display': tasks_to_display}
    return render(request, 'student/view_submit_task.html', context)


@login_required
def view_assigned_students_tasks(request):
    teacher = request.user

    assignments = Assignment.objects.filter(user_teacher=teacher)

    tasks_submissions = TaskSubmission.objects.filter(user_member__assignment__in=assignments)

    context = {'tasks_submissions': tasks_submissions}
    return render(request, 'teacher/view_assigned_students_tasks.html', context)



@login_required
def view_submitted_pdf(request, submission_id):
    submission = get_object_or_404(TaskSubmission, id=submission_id)
    if submission.submitted_task_file and submission.submitted_task_file.name.lower().endswith('.pdf'):
        return FileResponse(submission.submitted_task_file, content_type='application/pdf')
    else:
        return render(request, 'error.html', {'error_message': 'No PDF file available.'})




















