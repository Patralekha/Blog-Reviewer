# Generated by Django 3.0.8 on 2020-08-20 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsys', '0011_auto_20200820_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='blogimage',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
