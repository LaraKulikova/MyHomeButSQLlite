# Generated by Django 3.2.25 on 2024-10-01 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0010_auto_20241001_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='carexpense',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
