# Generated by Django 2.1.3 on 2018-12-25 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0002_auto_20181224_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='device_name',
            field=models.CharField(default='xingkongbaohe', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='devices',
            name='group',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='devices',
            name='add_datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='devices',
            name='last_register_datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login_datetime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='regist_datetime',
            field=models.DateTimeField(),
        ),
    ]