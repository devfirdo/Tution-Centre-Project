from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser 

class CustomUser(AbstractUser):
    user_type = models.CharField(default = 1, max_length=10)

class Courses(models.Model):
    course_name = models.CharField(max_length=255,null=True)
    syllabus = models.FileField(upload_to='uploads/',null=True,blank=True)
    course_fee = models.IntegerField(null=True)
    course_duration = models.CharField(max_length=255,null=True)    
    def get_syllabus_url(self):
        if self.syllabus:
            return self.syllabus.url
        return ''


class Usermembers(models.Model):
    user_course = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True)
    user_member = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    age = models.IntegerField()
    number = models.IntegerField()
    image = models.ImageField(blank=True,upload_to='images/',null=True)
    def current_assignment(self):
        return self.assignment_set.last()

class Assignment(models.Model):
    user_member = models.ForeignKey(Usermembers, on_delete=models.CASCADE)
    user_teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

class Teacherattendance(models.Model):
    teacher_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    attendance = models.CharField(max_length=20)

class StudentAttendance(models.Model):
    student_name = models.ForeignKey(Usermembers, on_delete=models.CASCADE)
    date = models.DateField()
    attendance = models.CharField(max_length=20)


class Task(models.Model):
    task_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.task_name

class TaskSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user_member = models.ForeignKey(Usermembers, on_delete=models.CASCADE)
    submitted_task_file = models.FileField(upload_to='submitted_tasks/', null=True, blank=True)




