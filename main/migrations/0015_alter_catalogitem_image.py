# Generated by Django 3.2.9 on 2021-12-06 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_review_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogitem',
            name='image',
            field=models.ImageField(default=None, upload_to='img'),
        ),
    ]