# Generated by Django 5.2.1 on 2025-06-12 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_customuser_created_at_customuser_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
