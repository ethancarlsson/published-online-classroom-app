'''
Model forms.
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Classroom, Company, Teacher, File,TopicDescription, Videos



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ManageClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'company',
                    'classroom_capacity', 'students', 'price', 'teacher',
                    'class_days', 'start_time', 'end_time',
                    'how_many_weeks', 'how_many_times',
                    ]


class AddCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'employee_name']

class MakeTeacher(ModelForm):
    class Meta:
        model = Teacher
        fields = ['name']


class UploadFile(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file_upload']

class DescriptionField(ModelForm):
    class Meta:
        model = TopicDescription
        fields = ['description']



class UploadVideoLink(ModelForm):
    '''
    For uploading videos into iframes
    '''
    class Meta:
        model = Videos
        fields = ['video_link']
