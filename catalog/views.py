from django.shortcuts import render
from .forms import ContactForm
from .models import Product, Contact


def index(request):
    latest_products = Product.objects.order_by('-created_at')[:5]

    for product in latest_products:
        print(f'Product: {product.name}, Created at: {product.created_at}')

    return render(request, 'catalog/index.html', {'latest_products': latest_products})


def catalog(request):
    return render(request, 'catalog/catalog.html')


def about(request):
    return render(request, 'catalog/about.html')


def contact_view(request):
    success_message = ""
    contact_info = Contact.objects.first()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            success_message = f"Привет, {name}! Ваше сообщение было успешно отправлено!"
            form = ContactForm()
    else:
        form = ContactForm()

    context = {
        'form': form,
        'success_message': success_message,
        'contact_info': contact_info,
    }
    return render(request, 'catalog/contact.html', context)
