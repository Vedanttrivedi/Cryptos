# Generated by Django 4.0 on 2022-03-09 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Discussion', '0005_auto_20211219_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disanswer',
            name='image',
            field=models.ImageField(default='media/answer.jpg', null=True, upload_to='discussion-pics'),
        ),
    ]
