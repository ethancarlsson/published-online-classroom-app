from django.contrib import admin

from .models import Teacher, Classroom, Company, File, TopicDescription, Videos, Week

@admin.register(Classroom)
class ClassAdmin(admin.ModelAdmin):
    pass

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

@admin.register(TopicDescription)
class TopicDescriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    pass

@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    pass