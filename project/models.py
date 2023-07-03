import uuid
from django.contrib.auth.models import User
from django.db import models
import random
from django.core.exceptions import ValidationError

def validate_image_file(value):
    if not value.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        raise ValidationError("Invalid file format. Only JPG, JPEG, PNG, and GIF files are allowed.")

    
class Teacher(models.Model):
    name = models.CharField(max_length=10, blank=True, null=False, default="john")
    lastname = models.CharField(max_length=10, blank=True, null=False, default="doe")
    profileImage = models.ImageField(null=True, blank=True, upload_to='static/Teacher/Images/', default="static/Teacher/Images/profile-icon-design-free-vector.jpg", validators=[validate_image_file])
    description = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return (self.name + " " + self.lastname) 

class PythonCourse(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instructor = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=False, blank=False)
    price = models.IntegerField(default=1, blank="false", null=False)

    
    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                generated_id = random.randint(1000, 9999)  # Generate a random 4-digit number
                if not PythonCourse.objects.filter(id=generated_id).exists():
                    self.id = generated_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Video(models.Model):
    course = models.ForeignKey(PythonCourse, on_delete=models.CASCADE, related_name='videos',)
    file = models.FileField(upload_to='static/videos/', null=False)
    title = models.CharField(max_length=100, null=True, default=course)
    id = models.AutoField(primary_key=True, editable=False, unique=True)


    def __str__(self):
        return f"{self.title}"
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='static/profile/Images/', default="static/Teacher/Images/profile-icon-design-free-vector.jpg", validators=[validate_image_file])
    date_of_birth = models.DateField(null=True)
    last_logged_in = models.DateTimeField(auto_now=True)
    user_created = models.DateTimeField(auto_now_add=True)
    purchases = models.ManyToManyField(PythonCourse, through='Purchase')
    
    def __str__(self):
        return self.user.username
    

    
class Purchase(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(PythonCourse, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} - {self.course.title}'
    
class CourseEnrollment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(PythonCourse, on_delete=models.CASCADE, related_name='enrollments')
    completed = models.BooleanField(default=False)
    progress = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.profile.user.username} - {self.course.title}'

    def save(self, *args, **kwargs):
        if self.progress >= 10:
            self.completed = True
        else:
            self.completed = False
        super().save(*args, **kwargs)