# Generated by Django 4.2.2 on 2023-07-01 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_alter_profile_profileimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='pythoncourse',
            name='instructor',
            field=models.CharField(default='John doe', max_length=100),
        ),
    ]