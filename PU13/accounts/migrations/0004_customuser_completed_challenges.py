# Generated by Django 3.0.3 on 2020-03-15 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_customuser_is_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='completed_challenges',
            field=models.IntegerField(null=True),
        ),
    ]
