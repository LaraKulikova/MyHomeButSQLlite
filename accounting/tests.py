import os

from django.utils.datetime_safe import date

from .forms import IncomeForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjectMyHomeBuh.settings')

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Income, Expense
from datetime import date


class IndexViewTests(TestCase):
    # 1.Создаю пользователя testuser с паролем 12345
    def setUp(self):
        username = 'testuser'
        password = '12345'
        self.user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        print(f'Создан пользователь {username} с паролем {password}')

    # 2.Проверяю отображение главной страницы без данных
    def test_index_view_with_no_data(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Домашняя бухгалтерия')
        self.assertQuerysetEqual(response.context['incomes'], [])
        self.assertQuerysetEqual(response.context['expenses'], [])
        print("Тест проверил отображение главной страницы без данных. Проверка пройдена успешно.")

    # 2.Проверяю отображение главной страницы с данными.
    def test_index_view_with_data(self):
        Income.objects.create(user=self.user, amount=1000, date=date.today())
        Expense.objects.create(user=self.user, amount=500, category='food', date=date.today())
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_income'], 1000)
        self.assertEqual(response.context['total_expenses_by_category'][0]['total'], 500)
        print("Тест проверил отображение главной страницы с данными. Проверка пройдена успешно.")


class AddIncomeViewTests(TestCase):
    # 1. Создаю пользователя testuser с паролем 12345
    def setUp(self):
        username = 'testuser'
        password = '12345'
        self.user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        print(f'Создан пользователь {username} с паролем {password}')

    # 2. Проверяю доступность страницы добавления дохода.
    def test_add_income_view_get(self):
        response = self.client.get(reverse('add_income'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], IncomeForm)
        print("Тест проверил доступность страницы добавления дохода. Проверка пройдена успешно.")

    # 3. Проверяю добавление дохода через POST-запрос..
    def test_add_income_view_post(self):
        data = {'amount': 1000, 'date': date.today(), 'category': 'salary'}
        response = self.client.post(reverse('add_income'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Income.objects.count(), 1)
        self.assertEqual(Income.objects.first().amount, 1000)
        print("Тест проверил добавление дохода через POST-запрос. Проверка пройдена успешно.")


class UserLoginViewTests(TestCase):
    # 1. Создаю пользователя testuser с паролем 12345
    def setUp(self):
        username = 'testuser'
        password = '12345'
        self.user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)
        print(f'Создан пользователь {username} с паролем {password}')

    # 2. Проверяю доступность страницы входа.
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        print("Тест проверил доступность страницы входа. Проверка пройдена успешно.")

    # 3. Проверяю вход с правильными данными
    def test_login_view_post_valid(self):
        data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        print("Тест проверил вход с правильными данными. Проверка пройдена успешно.")

    # 4. Проверяю вход с неправильными данными
    def test_login_view_post_invalid(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Данный пользователь не существует. Зарегистрировать пользователя?')
        print("Тест проверил вход с неправильными данными. Проверка пройдена успешно.")