# Generated by Django 3.2.10 on 2021-12-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='/static/blogindex.jpg', null=True, upload_to=''),
        ),
    ]
