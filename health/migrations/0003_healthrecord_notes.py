# Generated by Django 5.2 on 2025-06-06 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0002_alter_healthrecord_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthrecord',
            name='notes',
            field=models.TextField(blank=True, help_text='其他备注信息', null=True),
        ),
    ]
