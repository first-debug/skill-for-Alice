# Generated by Django 4.1.7 on 2023-03-27 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_userdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='recent_names',
            field=models.TextField(default=''),
        ),
    ]