# Generated by Django 4.2.5 on 2023-09-26 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daangn_app', '0011_remove_chatroom_user_chatroom_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
