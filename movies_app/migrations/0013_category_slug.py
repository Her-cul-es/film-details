# Generated by Django 4.2.13 on 2024-06-11 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0012_rename_text_review_review_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
