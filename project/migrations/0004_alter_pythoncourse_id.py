# Generated by Django 4.2.2 on 2023-06-28 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_pythoncourse_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pythoncourse',
            name='id',
            field=models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]