from django.contrib import admin
from . models import Profile,Course,Chapter,Lesson,CourseEnrollment

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(CourseEnrollment)
