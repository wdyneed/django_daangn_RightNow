# Generated by Django 4.2.5 on 2023-09-26 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daangn_app', '0010_remove_post_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='user',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='daangn_app.userinfo'),
        ),
    ]
