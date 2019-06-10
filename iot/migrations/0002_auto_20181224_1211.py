# Generated by Django 2.1.3 on 2018-12-24 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='devices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=16)),
                ('sn_code', models.CharField(max_length=128)),
                ('key', models.CharField(max_length=128)),
                ('bind_user', models.CharField(max_length=11)),
                ('add_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_register_datetime', models.DateTimeField(auto_now_add=True)),
                ('register_count', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='api_key',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='api_secret',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='login_numbers',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
