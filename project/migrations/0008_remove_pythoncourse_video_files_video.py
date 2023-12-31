# Generated by Django 4.2.2 on 2023-06-29 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_remove_profile_video_files_pythoncourse_video_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pythoncourse',
            name='video_files',
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='videos/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='project.pythoncourse')),
            ],
        ),
    ]
