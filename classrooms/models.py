'''
Classroom models.
'''
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from django.core.validators import MaxValueValidator



# used to define teachers
class Teacher(models.Model):
    '''
    Model to define teachers.
    '''
    name = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

## This will be used to create further flexibility when defining access to classrooms
class Company(models.Model):
    '''
    Model to define companies.
    '''
    name = models.CharField(default='some company', max_length=200, unique=True)
    employee_name = models.ManyToManyField(User)

    def get_absolute_url(self):
        return reverse('manage-companies')

    def __str__(self):
        return self.name


class Classroom(models.Model):
    ''''
    A model to build classrooms. It answers the following questions:
    - How many students can be in the room.
      - Which students are in the room.
      - Price for access to the room.
      - Which teacher(s) are assigned to the room
      - When will the class start and end.
      - When will students be able to sign up.
      - When will the classroom be closed.
    '''

    today = now
    weekdays = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    name = models.CharField(default='classroom', max_length=200, unique=True)
    open_for_public = models.BooleanField(verbose_name='Anyone can sign up for this class',
        default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    classroom_capacity = models.PositiveIntegerField()
    students = models.ManyToManyField(User)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    teacher = models.ManyToManyField(Teacher, default=4)
    class_days = models.CharField(
        max_length=20,
        choices=weekdays,
        default='Monday'
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    how_many_weeks = models.PositiveIntegerField(default=32, verbose_name='How many classes?')
    how_many_times = models.PositiveIntegerField(default=1, verbose_name='How many times a week?', validators=[MaxValueValidator])

    def get_absolute_url(self):
        return reverse('manage-classrooms')

    def __str__(self):
        return self.name

class Week(models.Model):
    '''
    Each classroom is split into weeks that are for holding content, such as files and videos.
    '''
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    week = models.IntegerField()
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.classroom)} week: {str(self.week)}'

class File(models.Model):
    '''
    Model to upload files to.
    '''
    name = models.CharField(max_length=50)
    file_upload = models.FileField(upload_to='media')
    week = models.ForeignKey(Week, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + '.' + str(str(self.file_upload).split('.')[1])

class TopicDescription(models.Model):
    '''
    Describe the topic of the week.
    '''
    description = models.TextField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE)


    def __str__(self):
        return self.description

class Videos(models.Model):
    '''
    A model for adding youtube videos to the classroom.
    '''
    video_link = models.CharField(max_length=200)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)

    def __str__(self):
        return self.video_link
