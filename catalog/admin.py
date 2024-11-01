from django.contrib import admin
from .models import Category, Product, Contact, Feedback


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Отображаем ID и название категории


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  # Отображаем ID, название, цену и категорию продукта
    list_filter = ('category',)  # Фильтрация по категории
    search_fields = ('name', 'description')  # Поиск по имени и описанию


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('address', 'email', 'phone')  # Отображаем ID, имя, email, телефон и сообщение
    search_fields = ('email', )  # Поиск по email


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
