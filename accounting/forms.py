from django import forms
from django.contrib.auth.models import User

from .models import Expense, CarExpense, Income, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class IncomeForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата')

    class Meta:
        model = Income
        fields = ['amount', 'category', 'date']


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата')

    class Meta:
        model = Expense
        fields = ['amount', 'category', 'subcategory', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].widget = forms.Select()
        if self.instance and self.instance.pk:
            self.fields['subcategory'].queryset = Expense.SUBCATEGORY_CHOICES.get(self.instance.category, [])
        else:
            self.fields['subcategory'].queryset = Expense.SUBCATEGORY_CHOICES.get(None, [])

    class Media:
        js = ('js/dynamic_subcategories.js',)


class CarExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата')

    class Meta:
        model = CarExpense
        fields = ['car_name', 'mileage', 'date', 'amount', 'subcategory']


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        max_length=150,
        help_text=_(
            '<span style="color: red; font-size: 12px;">'
            '<b>Обязательное поле.</b>'
            '</span>'
            '<ul style="color: red; font-size: 10px;">'
            '<b>Имя пользователя должно быть:</b>'
            '<li>Не более 150 символов</li>'
            '<li>Только буквы, цифры</li>'
            '<li>@/./+/-/_</li>'
            '</ul></span>'
        )
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput,
        help_text=_(
            '<span style="color: red; font-size: 12px;">'
            '<b>Обязательное поле.</b>'
            '</span>'
            '<ul style="color: red; font-size: 10px;">'
            '<b>Ваш пароль:</b>'
            '<li>Не должен совпадать и именем пользователя полностью или частично.</li>'
            '<li>Должен содержать не менее 8 символов.</li>'
            '<li>Должен содержать буквы, цифры и специальные символы. '
            '<li>Не должен состоять только из цифр или букв.</li>'
            '<li>Не должен быть слишком распространенным паролем.</li>'
            '</ul>'
            '</span>'
        ))
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput,
        help_text=_(
            '<span style="color: red; font-size: 10px;">'
            "Введите Ваш пароль еще раз."
            '</span>'
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Пользователь с таким именем уже существует."))
        return username


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'middle_name', 'phone']