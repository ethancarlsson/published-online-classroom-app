"""classroomsonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from classrooms import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Classroom content
    path('', views.home, name='home'), # The home page.
    path('classroom/<int:classroom_id>',
        views.StudentClassroom.as_view(), name='classroom'), # Path to the classroom.
    path('classroom-signup/<int:classroom_id>',
        views.sign_up, name='classroom-signup'),  #sign up for classroom
    path('teacher-classroom/<int:classroom_id>',
        views.TeacherClassroom.as_view(), name='teacher-classroom'), #teacher view

    # Registration and user auth
    path('register/', views.register_page, name='register'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #administrative
        #classrooms
    path('administration/', views.administration, name='administration'),
    path('administration/create-new-class/',
        views.create_new_classroom, name='create-new-class'),
    path('administration/edit-classroom/<int:classroom_id>/',
        views.edit_classroom, name='edit-classroom'),
        #companies
    path('administration/manage-companies/', views.manage_companies, name='manage-companies'),
    path('administration/manage-companies/add-new-company/',
        views.add_new_company, name='add-new-company'),

    path('administration/manage-companies/edit-company/<int:company_id>/',
        views.edit_company, name='edit-company'),
        #teachers
    path('administration/manage-teachers/', views.manage_teachers, name='manage-teachers'),
    path('administration/manage-teachers/create-new-teacher',
        views.add_new_teacher, name='create-new-teacher'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
