from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .forms import ContactForm, ProductForm
from .models import Product, Contact, Feedback, Category


class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'latest_products'
    queryset = Product.objects.order_by('created_at')[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['latest_products']:
            print(f'Product: {product.name}, Created at: {product.created_at}')
        return context


class CatalogView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'


class AboutView(TemplateView):
    template_name = 'catalog/about.html'


class ContactView(View):
    template_name = 'catalog/contact.html'

    def get(self, request, *args, **kwargs):
        contact_info = Contact.objects.first()
        form = ContactForm()
        context = {
            'form': form,
            'success_message': '',
            'contact_info': contact_info
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        contact_info = Contact.objects.first()
        form = ContactForm(request.POST)
        success_message = ""

        if form.is_valid():
            feedback = Feedback(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                message=form.cleaned_data.get('message')
            )
            feedback.save()
            success_message = f"Привет, {feedback.name}! Ваше сообщение было успешно отправлено!"
            form = ContactForm()

        context = {
            'form': form,
            'success_message': success_message,
            'contact_info': contact_info
        }
        return render(request, self.template_name, context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        product = form.save()
        return redirect('catalog:product_detail', product_id=product.id)
