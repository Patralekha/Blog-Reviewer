# Generated by Django 3.0.8 on 2020-08-19 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsys', '0009_auto_20200819_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='blogimage',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
