# Generated by Django 4.2.2 on 2023-07-01 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_pythoncourse_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='john', max_length=10)),
                ('lastname', models.CharField(blank=True, default='doe', max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='pythoncourse',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='project.teacher'),
        ),
    ]
