# Generated by Django 4.2.2 on 2023-07-01 19:56

from django.db import migrations, models
import project.models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_teacher_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profileImage',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='static/Teacher/Images/profile-icon-design-free-vector.jpg', null=True, upload_to='static/profile/Images/', validators=[project.models.validate_image_file]),
        ),
    ]
