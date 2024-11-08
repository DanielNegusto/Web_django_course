from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def product_image(product):
    """Возвращает HTML-код для отображения изображения продукта или название продукта, если изображение отсутствует."""
    path = product.image  # Получаем путь к изображению
    product_name = product.name  # Получаем название продукта

    if path:
        return f'<img src="{settings.MEDIA_URL}{path}" alt="{product_name}" class="product-image">'
    return f'<span>Нет изображения</span>'