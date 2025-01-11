# Generated by Django 3.1.12 on 2025-01-11 15:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_auto_20250111_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applyleave',
            name='total_leave',
        ),
        migrations.AddField(
            model_name='applyleave',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applyleave',
            name='staus',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applyleave',
            name='total_days',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='leave_annual',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='leave_casual',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='leave_medical',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='leave_other',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='applyleave',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='applyleave',
            name='leave_type',
            field=models.TextField(),
        ),
    ]
