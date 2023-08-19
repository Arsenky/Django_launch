from django.contrib import admin 

from mainapp import models as mainapp_models 

from django.utils.translation import gettext_lazy as _

@admin.register(mainapp_models.News) 
class NewsAdmin(admin.ModelAdmin): 
    list_display = ["id", "title", "deleted"]

@admin.register(mainapp_models.Lesson) 
class LessonAdmin(admin.ModelAdmin): 
    list_display = ["id", "get_course_name", "num", "title", "deleted"] 
    ordering = ["-course__name", "-num"] 
    list_per_page = 5
    search_fields = ["title", "preambule", "body"]
    actions = ["mark_deleted"]
    
    def get_course_name(self, obj): 
        return obj.course.name 
        
    get_course_name.short_description = ("Course")

    def mark_deleted(self, request, queryset): 
        queryset.update(deleted=True) 
        
    mark_deleted.short_description = ("Mark deleted")

@admin.register(mainapp_models.Courses) 
class CoursesAdmin(admin.ModelAdmin): 
    pass