from rest_framework import serializers
from project.models import *


class PythonCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PythonCourse
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'