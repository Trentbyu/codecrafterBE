# Generated by Django 4.2.2 on 2023-06-29 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_remove_profile_courses_alter_profile_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='video_files',
            field=models.FileField(null=True, upload_to='videos/'),
        ),
    ]
