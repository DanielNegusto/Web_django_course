from django.shortcuts import render
from .forms import ContactForm


def index(request):
    return render(request, 'catalog/index.html')


def catalog(request):
    return render(request, 'catalog/catalog.html')


def about(request):
    return render(request, 'catalog/about.html')


def contact_view(request):
    success_message = ""
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
    }
    return render(request, 'catalog/contact.html', context)
