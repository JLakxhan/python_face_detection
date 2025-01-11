# Generated by Django 3.1.12 on 2025-01-11 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_applyleave'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='contact_number',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='emergency_contact_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='emergency_contact_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='emergency_contact_relationship',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='employee_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='identity_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='joined_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='passport_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='personal_email',
            field=models.TextField(blank=True, null=True),
        ),
    ]
