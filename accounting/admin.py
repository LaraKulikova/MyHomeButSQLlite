from django.contrib import admin
from .models import Income, Expense, CarExpense, UserProfile

# Register your models here.
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(CarExpense)
admin.site.register(UserProfile)
