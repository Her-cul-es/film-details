# Generated by Django 4.2.13 on 2024-06-07 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0005_alter_userprofile_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mail',
            field=models.EmailField(blank=True, max_length=200),
        ),
    ]
