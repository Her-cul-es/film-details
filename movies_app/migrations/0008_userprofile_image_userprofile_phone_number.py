# Generated by Django 4.2.13 on 2024-06-08 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0007_remove_userprofile_mail_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.IntegerField(blank=True, max_length=10, null=True),
        ),
    ]