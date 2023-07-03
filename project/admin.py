
# Register your models here.
from .models import Profile, CourseEnrollment, PythonCourse, Purchase, Video, Teacher
from django.contrib import admin

admin.site.register(Profile)
admin.site.register(CourseEnrollment)
admin.site.register(PythonCourse)
admin.site.register(Purchase)
admin.site.register(Video)
admin.site.register(Teacher)




