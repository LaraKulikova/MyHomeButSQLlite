# Generated by Django 3.2.25 on 2024-09-26 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_alter_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('utilities', 'Коммунальные платежи'), ('communication', 'Мобильная связь, интернет, телевидение'), ('loan', 'Оплата кредита'), ('transport', 'Расходы на транспорт'), ('food', 'Продукты питания'), ('cleaning', 'Бытовая химия'), ('entertainment', 'Развлечения'), ('other', 'Прочие расходы')], max_length=20, verbose_name='Категория'),
        ),
    ]
