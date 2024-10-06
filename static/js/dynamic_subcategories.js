document.addEventListener('DOMContentLoaded', function() {
const categorySelect = document.getElementById('id_category');
const subcategorySelect = document.getElementById('id_subcategory');

const subcategories = {
'utilities': [
{value: 'electricity', text: 'Электроэнергия'},
{value: 'rent', text: 'Квартплата'},
{value: 'tax', text: 'Налог на квартиру'}
],
'communication': [
{value: 'mobile', text: 'Мобильная связь'},
{value: 'tv', text: 'Телевидение'},
{value: 'phone', text: 'Домашний телефон'},
{value: 'internet', text: 'Интернет'}
],
'loan': [
{value: 'consumer_loan', text: 'Кредит на потребительские нужды'},
{value: 'installment', text: 'Рассрочка'},
{value: 'car_loan', text: 'Кредит на покупку автомобиля'},
{value: 'housing_loan', text: 'Кредит на покупку жилья'}
],
'transport': [
{value: 'public_transport', text: 'Общественный транспорт'}, {value: 'bike', text: 'Расходы на ремонт и обслуживание велосипеда'},
{value: 'car_service', text: 'Расходы на ремонт и ТО автомобиля (без запчастей)'},
{value: 'spare_parts', text: 'Покупка запчастей и расходных материалов'},
{value: 'atocosmetics', text: 'Автокосметика'},
{value: 'carwash', text: 'Мойка и уборка автомобиля'},
{value: 'other_for_car', text: 'Другие расходы на автомобиль'}
],
'food': [
{value: 'bread', text: 'Хлеб, выпечка'},
{value: 'milk_eggs', text: 'Молоко, яйца'},
{value: 'frozen_food', text: 'Замороженные полуфабрикаты'},
{value: 'meat_poultry', text: 'Мясо, птица, колбасы'},
{value: 'fish_seafood', text: 'Рыба и морепродукты'},
{value: 'coffee_tea', text: 'Кофе, чай'},
{value: 'water_drinks', text: 'Вода, напитки'},
{value: 'grains_pasta_sugar', text: 'Крупы, макароны, сахар'},
{value: 'chips_nuts_snacks', text: 'Чипсы, орехи, снеки'},
{value: 'chocolate_candies', text: 'Шоколад, конфеты'},
{value: 'pet_food', text: 'Еда для домашнего любимца'},
{value: 'other_goods', text: 'Прочие товары'}
],
'cleaning': [
{value: 'laundry', text: 'Средства для стирки'},
{value: 'cleaning', text: 'Средства для уборки'},
{value: 'fertilizers', text: 'Удобрения'},
{value: 'other_chemicals', text: 'Прочая химия'}
],
'entertainment': [
{value: 'sports', text: 'Спорт'},
{value: 'travel', text: 'Путешествия'},
{value: 'cinema_theater', text: 'Кино, театры'},
{value: 'restaurants_cafes', text: 'Рестораны, кафе'},
],
'other': [
{value: 'education', text: 'Обучение'},
{value: 'miscellaneous', text: 'Иное'}
]
};

categorySelect.addEventListener('change', function() {
const selectedCategory = this.value;
const options = subcategories[selectedCategory] || [];

subcategorySelect.innerHTML = '';
options.forEach(function(option) {
const opt = document.createElement('option');
opt.value = option.value;
opt.text = option.text;
subcategorySelect.appendChild(opt);
});
});

// Trigger change event to populate subcategories on page load
categorySelect.dispatchEvent(new Event('change'));
});