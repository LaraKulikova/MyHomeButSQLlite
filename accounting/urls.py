
from django.urls import path
from django.conf.urls.static import static
from djangoProjectMyHomeBuh import settings
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.user_login, name='login'),
    path('index/', views.index, name='index'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('register/', views.register, name='register'),
    path('edit_expense/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('edit_income/<int:pk>/', views.edit_income, name='edit_income'),
    path('delete_expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('delete_income/<int:id>/', views.delete_income, name='delete_income'),
    path('get_subcategories/<str:category>/', views.get_subcategories, name='get_subcategories'),
    path('expenses/', views.expenses, name='expenses'),
    path('incomes/', views.incomes, name='incomes'),
    path('info/', views.info, name='info'),
    path('all_data_expenses/', views.all_data_expenses, name='all_data_expenses'),
    path('all_data_car/<int:expense_id>/', views.all_data_car, name='all_data_car'),
    path('add_car_expense/', views.add_car_expense, name='add_car_expense'),
    path('all_data_car/', views.all_data_car, name='all_data_car'),
    path('update_car_expenses/', views.update_car_expenses, name='update_car_expenses'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('personal_data/', views.personal_data, name='personal_data'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
