from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from classrooms.models import Classroom, Teacher

@login_required(login_url='login')
def home(request):
    teacher_group = Group.objects.get(name='Teachers')
    logged_in_user = request.user
    is_teacher = False

    classroom_list = Classroom.objects.filter(students=logged_in_user)
    if request.user in list(teacher_group.user_set.all()): # check to see if the user is a teacher
        is_teacher = True
        teacher = Teacher.objects.get(name=logged_in_user)
        classroom_list = Classroom.objects.filter(name=teacher)

    classes_without_student = Classroom.objects.exclude(students=logged_in_user)

    signup_list = []
    for classroom in classes_without_student:
        if classroom.students.count() != classroom.classroom_capacity:  # make sure the class isn't full
            if logged_in_user.groups.filter(name=classroom.company).exists() == True: # make sure the classroom is available to the student's company
                if classroom.name != 'Admin':                 # make sure the classroom isn't 'Admin'
                    signup_list.append(classroom)

    context = {'classroom_list': classroom_list, 'signup_list': signup_list, 'is_teacher': is_teacher}
    return render(request, 'classrooms/home.html', context)
