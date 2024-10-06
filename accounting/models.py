from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator


class Income(models.Model):
    CATEGORY_CHOICES = [
        ('salary', 'Зарплата'),
        ('credit', 'Кредит'),
        ('deposit', 'Депозит'),
        ('other', 'Прочие доходы'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    date = models.DateField(verbose_name='Дата')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')

    def __str__(self):
        return f"{self.category}: {self.amount}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('utilities', 'Коммунальные платежи'),
        ('communication', 'Мобильная связь, интернет, телевидение'),
        ('loan', 'Оплата кредита'),
        ('transport', 'Расходы на транспорт'),
        ('food', 'Продукты питания'),
        ('cleaning', 'Бытовая химия'),
        ('entertainment', 'Развлечения'),
        ('other', 'Прочие расходы'),
    ]

    SUBCATEGORY_CHOICES = {
        'utilities': [
            ('electricity', 'Электроэнергия'),
            ('rent', 'Квартплата'),
            ('tax', 'Налог на квартиру'),
        ],
        'communication': [
            ('mobile', 'Мобильная связь'),
            ('tv', 'Телевидение'),
            ('phone', 'Домашний телефон'),
            ('internet', 'Интернет'),
        ],
        'loan': [
            ('consumer_loan', 'Кредит на потребительские нужды'),
            ('installment', 'Рассрочка'),
            ('car_loan', 'Кредит на покупку автомобиля'),
            ('housing_loan', 'Кредит на покупку жилья'),
        ],
        'transport': [
            ('public_transport', 'Общественный транспорт'),
            ('bike', 'Велосипед'),
            ('car_service', 'Расходы на ремонт и ТО автомобиля (без запчастей)'),
            ('spare_parts', 'Покупка запчастей и расходных материалов'),
            ('atocosmetics', 'Автокосметика'),
            ('carwash', 'Мойка и уборка автомобиля'),
            ('other_for_car', 'Другие расходы на автомобиль'),
        ],
        'food': [
            ('bread', 'Хлеб, выпечка'),
            ('milk_eggs', 'Молоко, яйца'),
            ('frozen_food', 'Замороженные полуфабрикаты'),
            ('meat_poultry', 'Мясо, птица, колбасы'),
            ('fish_seafood', 'Рыба и морепродукты'),
            ('coffee_tea', 'Кофе, чай'),
            ('water_drinks', 'Вода, напитки'),
            ('grains_pasta_sugar', 'Крупы, макароны, сахар'),
            ('chips_nuts_snacks', 'Чипсы, орехи, снеки'),
            ('chocolate_candies', 'Шоколад, конфеты'),
            ('pet_food', 'Еда для домашнего любимца'),
            ('other_goods', 'Прочие товары'),
        ],
        'cleaning': [
            ('laundry', 'Средства для стирки'),
            ('cleaning', 'Средства для уборки'),
            ('fertilizers', 'Удобрения'),
            ('other_chemicals', 'Прочая химия'),
        ],
        'entertainment': [
            ('sports', 'Спорт'),
            ('travel', 'Путешествия'),
            ('cinema_theater', 'Кино, театры'),
            ('restaurants_cafes', 'Рестораны, кафе'),
        ],
        'other': [
            ('education', 'Обучение'),
            ('miscellaneous', 'Иное'),
        ],
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    date = models.DateField(verbose_name='Дата')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    subcategory = models.CharField(max_length=20, verbose_name='Подкатегория', blank=True, null=True)

    def __str__(self):
        return f"{self.category}: {self.amount}"


class CarExpense(models.Model):
    car_name = models.CharField(max_length=100, blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.OneToOneField(
        'Expense',
        on_delete=models.CASCADE,
        related_name='car_expense',
        null=True,
        blank=True
    )
    note = models.TextField(blank=True, null=True)  # Новое поле для примечаний


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username
