# Generated by Django 5.0.6 on 2025-03-19 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('manager', 'Manager'), ('employee', 'Employee')], default='employee', max_length=10),
        ),
    ]
