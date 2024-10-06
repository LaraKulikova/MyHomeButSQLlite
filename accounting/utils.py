import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from .models import Expense


def generate_expense_graphs(user):
    # Получение данных из базы данных
    expenses = Expense.objects.filter(user=user).values('date', 'category', 'subcategory', 'amount')

    # Преобразование данных
    dates = np.array([expense['date'] for expense in expenses])
    dates = np.array([datetime.combine(expense_date, datetime.min.time()) if isinstance(expense_date, datetime) else expense_date for expense_date in dates])
    amounts = np.array([expense['amount'] for expense in expenses])

    # Построение графика расходов по датам
    plt.figure(figsize=(10, 5))
    plt.plot(dates, amounts, marker='o', linestyle='-', color='b', label='Expenses')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Expenses Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  # Поворот меток по оси X для лучшей читаемости
    plt.tight_layout()  # Для автоматической настройки границ графика
    plt.savefig('static/expenses_over_time.png')
    plt.close()  # Закрываем график, чтобы избежать наложения на следующий

    # Построение графика расходов по категориям
    categories = list(set(expense['category'] for expense in expenses))
    category_sums = [
        sum(expense['amount'] for expense in expenses if expense['category'] == category)
        for category in categories
    ]

    plt.figure(figsize=(10, 5))
    plt.pie(category_sums, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    plt.axis('equal')  # Чтобы круг был кругом
    plt.savefig('static/expenses_by_category.png')
    plt.close()  # Закрываем график