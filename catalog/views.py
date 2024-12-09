from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ContactForm, ProductForm
from .models import Product, Contact, Feedback, Category
from .services import get_products_by_category


class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'latest_products'
    queryset = Product.objects.order_by('-created_at')[:6]  # Сортировка по убыванию

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['latest_products']:
            print(f'Product: {product.name}, Created at: {product.created_at}')
        return context


class CatalogView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        cache_key = f'products_category_{category_id}' if category_id else 'all_products'

        products = cache.get(cache_key)

        if products is None:
            if category_id:
                products = get_products_by_category(category_id)
            else:
                products = super().get_queryset()
            cache.set(cache_key, products, 10)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Получаем все категории
        context['selected_category_id'] = self.request.GET.get('category_id')  # Передаем id выбранной категории
        return context


class AboutView(TemplateView):
    template_name = 'catalog/about.html'


class ContactView(View):
    template_name = 'catalog/contact.html'

    def get(self, request, *args, **kwargs):
        contact_info = Contact.objects.first()
        form = ContactForm()
        return render(request, self.template_name, {
            'form': form,
            'success_message': '',
            'contact_info': contact_info,
        })

    def post(self, request, *args, **kwargs):
        contact_info = Contact.objects.first()
        form = ContactForm(request.POST)
        success_message = ""

        if form.is_valid():
            feedback = Feedback.objects.create(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                message=form.cleaned_data.get('message')
            )
            success_message = f"Привет, {feedback.name}! Ваше сообщение было успешно отправлено!"
            form = ContactForm()

        return render(request, self.template_name, {
            'form': form,
            'success_message': success_message,
            'contact_info': contact_info,
        })


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_object(self, **kwargs):
        cache_key = f'product_{self.kwargs.get(self.pk_url_kwarg)}'
        product = cache.get(cache_key)

        if not product:
            product = super().get_object()
            cache.set(cache_key, product, timeout=300)  # Кэшируем на 5 минут (300 секунд)

        return product

    def post(self, request, *args, **kwargs):
        product = self.get_object()  # Получаем объект продукта, используя кэшированную версию

        # Проверяем, имеет ли пользователь право "can_unpublish_product"
        if not (request.user.has_perm('catalog.can_unpublish_product') or self.request.user == product.owner):
            messages.error(request, "У вас нет прав для выполнения этого действия.")
            return redirect('catalog:product_detail', product_id=self.kwargs.get(self.pk_url_kwarg))

        product.status = 'draft'  # Устанавливаем статус как "Черновик"
        product.save()
        messages.success(request, f"Продукт {product.name} был успешно снят с публикации.")

        # Очистить кэш после изменения продукта
        cache.delete(f'product_{product.id}')

        return redirect('catalog:product_detail', product_id=product.id)


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    pk_url_kwarg = 'product_id'

    def get_object(self):
        product = super().get_object()
        if not (self.request.user == product.owner or self.request.user.has_perm('catalog.change_product')):
            messages.error(self.request, "У вас нет прав для редактирования этого продукта.")
            raise PermissionDenied
        return product

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'product_id': self.object.id})


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/delete_product.html'
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self):
        product = super().get_object()

        # Проверка прав: либо владелец, либо с разрешением на удаление
        if not (self.request.user == product.owner or self.request.user.has_perm('catalog.delete_product')):
            messages.error(self.request, "У вас нет прав для удаления этого продукта.")
            raise PermissionDenied  # Это обеспечит правильный ответ 403

        return product
