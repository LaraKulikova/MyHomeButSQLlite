from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.db import models
from datetime import datetime, date
import decimal
import json
from django.db.models import Sum
from .utils import generate_expense_graphs
from .models import CarExpense
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserForm, UserProfileForm
from .forms import CustomUserCreationForm

# добавляю в гит все не получается
@login_required
def index(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total_income = sum(income.amount for income in incomes)
    total_expenses_by_category = expenses.values('category').annotate(total=models.Sum('amount'))

    return render(request, 'accounting/index.html', {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expenses_by_category': total_expenses_by_category
    })


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('incomes')
    else:
        form = IncomeForm()

    return render(request, 'accounting/income/add_income.html', {'form': form})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            # Проверка подкатегории
            if expense.category == 'transport' and expense.subcategory in [
                'car_service', 'spare_parts', 'atocosmetics', 'carwash', 'other_for_car'
            ]:
                return redirect('all_data_car', expense_id=expense.id)
            else:
                return redirect('expenses')
    else:
        form = ExpenseForm()

    return render(request, 'accounting/expense/add_expense.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'accounting/login.html',
                          {'error': 'Данный пользователь не существует. Зарегистрировать пользователя?'})

    return render(request, 'accounting/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounting/register.html', {'form': form})


from django.shortcuts import get_object_or_404, render, redirect
from .models import Expense
from .forms import ExpenseForm


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('incomes')  # Перенаправление на главную страницу или другую страницу после сохранения
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'accounting/expense/edit_expense.html', {'form': form})


def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk)

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)

        if form.is_valid():
            form.save()
            return redirect('expenses')  # Перенаправление на страницу расходов
    else:
        form = IncomeForm(instance=income)

    return render(request, 'accounting/income/edit_income.html', {'form': form})


def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expenses')


def delete_income(request, id):
    income = get_object_or_404(Income, id=id)
    income.delete()
    return redirect('incomes')


def get_subcategories(request, category):
    subcategories = Expense.SUBCATEGORY_CHOICES.get(category, [])
    return JsonResponse({'subcategories': [{'value': sub, 'display': sub} for sub in subcategories]})


def expenses(request):
    current_month = datetime.now().month
    current_year = datetime.now().year

    expenses = Expense.objects.filter(user=request.user)

    total_expenses_current_month = expenses.filter(
        date__month=current_month,
        date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expenses_all_time = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'expenses': expenses,
        'total_expenses_current_month': total_expenses_current_month,
        'total_expenses_all_time': total_expenses_all_time,
    }

    return render(request, 'accounting/expense/expenses.html', context)


# def incomes(request):
#     # Получение данных о доходах из базы данных
#     incomes = Income.objects.all()
#     total_income = sum(income.amount for income in incomes)
#
#     context = {
#         'incomes': incomes,
#         'total_income': total_income,
#     }
#     return render(request, 'accounting/income/incomes.html', context)
def incomes(request):
    # Получение данных о доходах текущего пользователя из базы данных
    incomes = Income.objects.filter(user=request.user)
    total_income = sum(income.amount for income in incomes)

    context = {
        'incomes': incomes,
        'total_income': total_income,
    }
    return render(request, 'accounting/income/incomes.html', context)


def info(request):
    # Логика для страницы информации
    return render(request, 'accounting/information/info.html')


def decimal_default(obj):
    print(f"Checking object: {obj} of type {type(obj)}")
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


@login_required
def all_data_expenses(request):
    generate_expense_graphs(request.user)

    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_incomes = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_balance = total_incomes - total_expenses

    context = {
        'expenses': json.dumps(list(expenses.values()), default=decimal_default),
        'incomes': json.dumps(list(incomes.values()), default=decimal_default),
        'total_expenses': total_expenses,
        'total_incomes': total_incomes,
        'total_balance': total_balance,
    }

    return render(request, 'accounting/information/all_data_expenses.html', context)




@login_required
def add_car_expense(request):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        mileage = request.POST.get('mileage')
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        subcategory = request.POST.get('subcategory')
        note = request.POST.get('note')

        CarExpense.objects.create(
            car_name=car_name,
            mileage=mileage,
            date=date,
            amount=amount,
            category='transport',
            subcategory=subcategory,
            user=request.user,
            note=note
        )
        return redirect('all_data_car')
    else:
        form = CarExpenseForm()
        return render(request, 'accounting/car_expense/add_car_expense.html', {'form': form})

@login_required
def all_data_car(request, expense_id):
    car_expenses = CarExpense.objects.filter(user=request.user)
    return render(request, 'accounting/information/all_data_car.html', {
        'car_expenses': car_expenses,
        'expense_id': expense_id
    })
def update_car_expenses(request):
    if request.method == 'POST':
        for expense in CarExpense.objects.filter(user=request.user):
            expense.car_name = request.POST.get(f'car_name_{expense.id}')
            mileage = request.POST.get(f'mileage_{expense.id}')
            expense.note = request.POST.get(f'note_{expense.id}')

            # Проверка и обработка пустых значений для mileage
            if mileage:
                expense.mileage = mileage
            else:
                expense.mileage = 0  # Или любое другое значение по умолчанию

            expense.save()
    return redirect('all_data_car', expense_id=expense.id)

# для страницы с персональными данными
def personal_data(request):
    return render(request, 'accounting/personal_data.html')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'accounting/personal_data.html', {
        'user': request.user,
        'user_form': user_form,
        'profile_form': profile_form
    })
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'accounting/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
