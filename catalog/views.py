from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
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


class UpdateProductView(LoginRequiredMixin, UpdateView):  # Добавляем LoginRequiredMixin
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})


class AddProductView(LoginRequiredMixin, CreateView):  # Добавляем LoginRequiredMixin
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class DeleteProductView(LoginRequiredMixin, DeleteView):  # Добавляем LoginRequiredMixin
    model = Product
    template_name = 'catalog/delete_product.html'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('catalog:catalog')
