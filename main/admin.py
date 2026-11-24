from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# admin.py
from django.contrib import admin
from .models import Notification

admin.site.site_header = "Department of Computer Science - Course Folder Portal"
admin.site.site_title = "CS Dept Admin"
admin.site.index_title = "Welcome to the Department of Computer Science Portal"

from django.contrib import admin
from django.utils.html import format_html
from django.forms import TextInput
from .models import TeacherDocument

class TeacherDocumentAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "color":  # Apply color picker only to the color field
            kwargs["widget"] = TextInput(attrs={"type": "color"})
        return super().formfield_for_dbfield(db_field, **kwargs)

  

admin.site.register(TeacherDocument, TeacherDocumentAdmin)

# admin.py

from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user',  'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username',  'message']

admin.site.register(Message)
admin.site.register(MidTermSolution)
admin.site.register(Subject)
admin.site.register(Year)
admin.site.register(SemesterType)

admin.site.register(TeacherProfile)

admin.site.register(SubjectComment)

admin.site.register(AcademicSchedule)
admin.site.register(CourseObjective)
admin.site.register(CourseOutline)
admin.site.register(WeeklyPlan)
admin.site.register(Timetable)
admin.site.register(MakeupClass)
admin.site.register(LectureNotes)
admin.site.register(ReferenceMaterial)
admin.site.register(Assignment)
admin.site.register(AssigmentMarks)

admin.site.register(Quiz)
admin.site.register(QuizMarks)

admin.site.register(Presentation)
admin.site.register(MidTermPaper)
admin.site.register(FinalTermPaper)
admin.site.register(FinalTermSolution)
admin.site.register(SessionalMarks)
admin.site.register(RecommendationsAndSuggestions)
admin.site.register(AttendanceRecord)

admin.site.register(CounselingHours)

