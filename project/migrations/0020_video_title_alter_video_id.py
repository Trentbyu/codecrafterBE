# Generated by Django 4.2.2 on 2023-07-02 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_alter_courseenrollment_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='title',
            field=models.CharField(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='project.pythoncourse'), max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
