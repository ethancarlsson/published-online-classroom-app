'''
This module handles everything related to classroom views.
'''

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.core.paginator import Paginator

from classrooms.decorators import allowed_users, restricted_access
from classrooms.models import Classroom, File, TopicDescription, Week, Videos
from classrooms.forms import UploadFile, DescriptionField, UploadVideoLink


class ClassroomView(View):
    '''
    Parent class for classrooms. Different kinds of classrooms inherit from
    this classroom so that there is no need to repeat shared context.
    '''
    def get_shared_context(self, request,  classroom_id):
        '''
        This method collects the shared context for different kinds of classroom
        views. It collects the classroom id, the hash and the classroom's uploaded content.
        '''
        classroom = Classroom.objects.get(pk=classroom_id)

        classroom_hash = hash(str(classroom))

        ordered_weeks = Week.objects.filter(classroom=classroom).order_by('week')

        paginator = Paginator(ordered_weeks, 1)

        unfinished_classes = [week for week in ordered_weeks if not week.finished]
        week_obj = Week.objects.get(classroom=classroom, week=unfinished_classes[0].week)


        page_number = request.GET.get('page')
        page_obj = paginator.get_page(week_obj.week)


        if page_number is not None:
            page_obj = paginator.get_page(page_number)
            week_obj = Week.objects.get(classroom=classroom, week=page_number)

        week_description = list(TopicDescription.objects.filter(week=week_obj))
        video_links = list(Videos.objects.filter(week=week_obj))
        files_for_week = list(File.objects.filter(week=week_obj))

        two_less = week_obj.week - 2
        two_more = week_obj.week + 2
        number_of_weeks = ordered_weeks.count()
        not_too_low = True
        not_too_high = True
        if two_less == 0:
            not_too_high = False

        if two_more == number_of_weeks:
            not_too_high = False

        context = {
            'classroom': classroom,
            'classroom_hash': classroom_hash,
            'page_obj': page_obj,
            'week_description': week_description,
            'video_links': video_links,
            'files_for_week': files_for_week,
            'week_obj': week_obj,
            'not_too_low': not_too_low,
            'not_too_high': not_too_high,
            'ordered_weeks': ordered_weeks,
            }

        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(), name='dispatch')
class StudentClassroom(ClassroomView):
    '''
    Classroom view that students should see. Content can be viewed but not created,
    uploaded or deleted.
    '''
    def get(self, request, classroom_id):
        '''
        Pulls shared context and renders the classroom html.
        '''
        context = ClassroomView.get_shared_context(self, request, classroom_id)
        teacher_group = Group.objects.get(name='Teachers')

        is_teacher = False
        if request.user in list(teacher_group.user_set.all()):
            is_teacher = True

        context.update({'is_teacher': is_teacher})


        return render(request, 'classrooms/classroom_views/classroom.html', context)

    def post(self, request, classroom_id):
        '''
        Used so that the student can remove themselves from the classroom.
        '''
        classroom = Classroom.objects.get(pk=classroom_id)
        if request.POST['Sign out of this class'] in request.POST:
            user = request.user
            classroom.students.remove(user)
            class_group = Group.objects.get(name=classroom)
            class_group.user_set.remove(user)

        return redirect('home')


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(restricted_access(allowed_roles=['Teachers']), name='dispatch')
class TeacherClassroom(ClassroomView):
    '''
    Classroom view for teachers. Allows teachers to create, update and delete.
    '''
    def teacher_context(self, request, classroom_id):
        '''Used to add more shared context'''

        context = ClassroomView.get_shared_context(self, request, classroom_id)

        form = UploadFile()
        description_form = DescriptionField()
        video_link_form = UploadVideoLink()

        context.update({
            'form': form,
            'description_form': description_form,
            'video_link_form': video_link_form,
            })
        context.update()
        return context



    def get(self, request, classroom_id):
        '''
        Get's shared context and adds additional context for CRUD functionality
        '''
        context = self.teacher_context(request, classroom_id)

        return render(request, 'classrooms/classroom_views/teacher_classroom.html', context)


    def post(self, request, classroom_id):
        '''
        Logic for all CRUD operations. File upload, deletion and posting/updating week description
        '''

        context = self.teacher_context(request, classroom_id)

        if len(request.FILES) >= 1:
            form = UploadFile(request.POST, request.FILES)
            number = context['week_obj']
            file_ = request.FILES['file_upload']
            file_name = request.POST['name']
            if form.is_valid():
                File.objects.create(week=number, name=file_name, file_upload=file_)

        elif 'Delete' in request.POST:
            file_to_delete = File.objects.get(id=request.POST['Delete'])
            file_to_delete.delete()

        elif 'Description' in request.POST:
            number = context['week_obj']
            description = request.POST['description']
            if DescriptionField(request.POST).is_valid():
                TopicDescription.objects.create(week=number, description=description)

        elif 'Delete description' in request.POST:
            file_to_delete = TopicDescription.objects.get(id=request.POST['Delete description'])
            file_to_delete.delete()

        elif 'Video_Link' in request.POST:
            video_link = request.POST['video_link']
            number = context['week_obj']
            video_link_form = UploadVideoLink(request.POST)
            if video_link_form.is_valid():
                Videos.objects.create(week=number, video_link=video_link)

        elif 'Delete video' in request.POST:
            video_to_delete = Videos.objects.get(id=request.POST['Delete video'])
            video_to_delete.delete()

        elif 'Class_finished' in request.POST:
            context['week_obj'].finished = True
            context['week_obj'].save()

        elif 'Class_opened' in request.POST:
            context['week_obj'].finished = False
            context['week_obj'].save()

        context = self.teacher_context(request, classroom_id)
        return render(request, 'classrooms/classroom_views/teacher_classroom.html', context)

def sign_up(request, classroom_id):
    '''
    View for signing up to a classroom.
    '''
    classroom = Classroom.objects.get(pk=classroom_id)

    if request.method == 'POST':
        if request.POST['Sign up'] in request.POST:
            user = request.user
            classroom.students.add(user)
            class_group = Group.objects.get(name=classroom)
            class_group.user_set.add(user)
            return redirect('home')

    context = {'classroom': classroom}

    return render(request, 'classrooms/classroom_views/classroom-signup.html', context)