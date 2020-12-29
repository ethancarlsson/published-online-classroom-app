from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required


from classrooms.decorators import restricted_access
from classrooms.forms import ManageClassroomForm, AddCompanyForm, MakeTeacher
from classrooms.models import Classroom, Company, Teacher, User, Week

from django.contrib.auth.models import Group
from django.views.generic import ListView


def deleter(request, target_objects):
    '''
    deletion utility function.
    '''
    target_name = request.POST.get('Delete')
    deletion_target = target_objects.get(name=target_name)
    deletion_target.delete()
    group_to_delete = Group.objects.get(name=target_name)
    group_to_delete.delete()


@login_required(login_url='login')
@restricted_access(allowed_roles=['Admin'])
def administration(request):
    '''
    View all admin data and options.
    '''

    classrooms = Classroom.objects.all()
    dashboard_data = []
    for room in classrooms:
        weeks = Week.objects.filter(classroom=room)
        amount_of_students = room.students.all().__len__()
        dashboard_data.append((
            room, weeks.__len__(),
            weeks.filter(finished=True).__len__(),
            amount_of_students,
            room.classroom_capacity,
            ))

    if request.method == 'POST':
        deleter(request, classrooms)
        return redirect('administration')


    context = {
        'dashboard_data': dashboard_data,
        }
    return render(request, 'classrooms/administration/administration.html', context)

#Create classroom
@login_required(login_url='login')
@restricted_access(allowed_roles=['Admin'])
def create_new_classroom(request):
    '''
    Where administrator can add new classrooms.
    '''
    ## Everything for creating the forms
    # gets the form
    form = ManageClassroomForm()
    if request.method == 'POST':
        form = ManageClassroomForm(request.POST)

        if form.is_valid():
            #save the classroom
            saved_form = form.save()

            #get students and teachers from the class
            students_attending = saved_form.students.all()
            teachers = saved_form.teacher.all()

            #create a new group
            new_group = Group.objects.create(name=request.POST['name'])

            # puts students in the group
            for student in students_attending:
                new_group.user_set.add(student)
            for teach in teachers:
                new_group.user_set.add(teach.name)

            # Create new week objects
            for week in range(saved_form.how_many_weeks):
                Week.objects.create(classroom=saved_form, week=week+1)
            return redirect('administration')

    context = {'form': form}
    return render(request, 'classrooms/administration/create-new-class.html', context)

def edit_classroom(request, classroom_id):
    instance = get_object_or_404(Classroom, pk=classroom_id)

    form = ManageClassroomForm(request.POST or None, instance=instance)
    if form.is_valid():
        classroom_name = request.POST['name']
        students = Classroom.objects.get(name=classroom_name).students.all()
        group = Group.objects.get(name=classroom_name)

        group.user_set.clear()

        for student in students:
            group.user_set.add(student)
        form.save()

        return redirect('administration')
    context = {'form': form}
    return render(request, 'classrooms/administration/edit-classroom.html', context)

#Companies
@login_required(login_url='login')
@restricted_access(allowed_roles=['Admin'])
def manage_companies(request):
    # assign all companies ot a variable
    all_companies = Company.objects.exclude(name='Anyone can sign up')

    if request.method == 'POST':
        deleter(request, all_companies)
        return redirect('manage-companies')

    context = {'all_companies': all_companies}
    return render(request, 'classrooms/administration/manage-companies.html', context)

@login_required(login_url='login')
@restricted_access(allowed_roles=['Admin'])
def add_new_company(request):
    '''
    For adding new companies.
    '''
    form = AddCompanyForm()
    if request.method == 'POST':
        form = AddCompanyForm(request.POST)

        if form.is_valid():
            #saves the company
            form.save()

            #gets students from the company
            company_name = request.POST['name']
            employees = Company.objects.get(name=company_name).employee_name.all()

            #creates a new group
            new_group = Group.objects.create(name=company_name)

            # puts students in the group
            for employee in employees:
                new_group.user_set.add(employee)

            return redirect('manage-companies')

    context = {'form': form}
    return render(request, 'classrooms/administration/create_new_company.html', context)

# solution found here:
# https://stackoverflow.com/questions/4673985/how-to-update-an-object-from-edit-form-in-django
def edit_company(request, company_id):
    '''
    For adding or removing employees from the company or if there is a name change.
    '''
    instance = get_object_or_404(Company, pk=company_id)

    form = AddCompanyForm(request.POST or None, instance=instance)
    group = Group.objects.get(name=instance.name)

    if form.is_valid():
        company_name = request.POST['name']

        form.save()
        employees = Company.objects.get(name=company_name).employee_name.all()

        group.name = company_name
        group.save()
        group.user_set.clear()

        for employee in employees:
            group.user_set.add(employee)

        return redirect('manage-companies')
    context = {'form': form}
    return render(request, 'classrooms/administration/edit-company.html', context)

## Teachers ##
@login_required(login_url='login')
@restricted_access(allowed_roles=['Admin'])
def manage_teachers(request):
    # assign all companies ot a variable
    all_teachers = Teacher.objects.all()

    if request.method == 'POST':
        post_dict = request.POST
        instruction = list(post_dict.items())[1]
        if instruction[1] == 'Delete':
            user_ = User.objects.get(username=instruction[0])

            teacher = all_teachers.get(name=user_.pk)
            teacher.delete()

            teacher_group = Group.objects.get(name='Teachers')
            teacher_group.user_set.remove(user_.pk)

            
    context = {'all_teachers': all_teachers}
    return render(request, 'classrooms/administration/manage-teachers.html', context)

def add_new_teacher(request):
    ## Everything for creating new teachers
    # gets the form
    form = MakeTeacher()
    feedback = ''
    if request.method == 'POST':
        form = MakeTeacher(request.POST)
        #gets teacher
        teacher = request.POST['name']
        if form.is_valid():
            #saves the company
            form.save()

            #gets teacher group
            teacher_group = Group.objects.get(name='Teachers')
            # puts teach in the teacher group
            teacher_group.user_set.add(teacher)

            feedback = 'This teacher has been added to the teacher group.'
        else:
            feedback = 'This teacher has already been added to the teacher group.'

    context = {'form': form, 'feedback': feedback}
    return render(request, 'classrooms/administration/create-new-teacher.html', context)
