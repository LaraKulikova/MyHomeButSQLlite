from .models import Expense, CarExpense, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=Expense)
def create_or_update_car_expense(sender, instance, created, **kwargs):
    car_subcategories = [
        'car_service',
        'spare_parts',
        'atocosmetics',
        'carwash',
        'other_for_car'
    ]

    if instance.subcategory in car_subcategories:
        CarExpense.objects.update_or_create(
            expense=instance,
            defaults={
                'date': instance.date,
                'amount': instance.amount,
                'category': instance.category,
                'subcategory': instance.subcategory,
                'user': instance.user
            }
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
