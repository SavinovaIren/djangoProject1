# Generated by Django 4.0.1 on 2023-01-07 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_tguser_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='tg_chat_id',
            field=models.BigIntegerField(verbose_name='id чата'),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='tg_user_id',
            field=models.BigIntegerField(unique=True, verbose_name='id пользователя'),
        ),
    ]