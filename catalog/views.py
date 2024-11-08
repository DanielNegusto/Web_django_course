from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm, ProductForm
from .models import Product, Contact, Feedback, Category


def index(request):
    latest_products = Product.objects.order_by('created_at')[:6]

    for product in latest_products:
        print(f'Product: {product.name}, Created at: {product.created_at}')

    return render(request, 'catalog/index.html', {'latest_products': latest_products})


def catalog(request):
    products = Product.objects.all()  # Извлекаем все продукты
    return render(request, 'catalog/catalog.html', {'products': products})


def about(request):
    return render(request, 'catalog/about.html')


def contact_view(request):
    success_message = ""
    # Получите первую запись контактов из базы данных
    contact_info = Contact.objects.first()  # Замените на нужный запрос, если у вас несколько записей

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохраните данные обратной связи
            feedback = Feedback(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                message=form.cleaned_data.get('message')
            )
            feedback.save()  # Сохраните объект обратной связи

            success_message = f"Привет, {feedback.name}! Ваше сообщение было успешно отправлено!"
            form = ContactForm()  # Сброс формы после успешной отправки
    else:
        form = ContactForm()

    context = {
        'form': form,
        'success_message': success_message,
        'contact_info': contact_info,  # Передайте информацию о контакте в контекст
    }
    return render(request, 'catalog/contact.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Используем get_object_or_404
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('catalog:product_detail', product_id=product.id)
    else:
        form = ProductForm()

    categories = Category.objects.all()  # Получаем все категории
    return render(request, 'catalog/add_product.html', {'form': form, 'categories': categories})
