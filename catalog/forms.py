from django import forms

from .models import Product, Category


class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Ваш email')
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)


FORBIDDEN_WORDS_NAME = [
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
                        ]
FORBIDDEN_WORDS_DESCRIPTION = [
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    new_category = forms.CharField(max_length=255, required=False, label="Новая категория")

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image', 'status']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название продукта'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание продукта'
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите цену продукта'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            required=False,  # Сделаем выбор категории необязательным
            label="Выберите категорию",
            empty_label="Выберите категорию или создайте новую"
        )

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get('new_category')
        category = cleaned_data.get('category')

        if new_category:
            # Если введена новая категория, создаем или находим её
            category, created = Category.objects.get_or_create(name=new_category)
            cleaned_data['category'] = category
        elif not category and not new_category:
            raise forms.ValidationError("Выберите категорию или создайте новую.")

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name', '').lower()
        for word in FORBIDDEN_WORDS_NAME:
            if word.lower() in name:
                raise forms.ValidationError(f"Имя продукта не должно содержать слово '{word}'.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '').lower()
        for word in FORBIDDEN_WORDS_DESCRIPTION:
            if word.lower() in description:
                raise forms.ValidationError(f"Описание продукта не должно содержать слово '{word}'.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена продукта не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Допустимые форматы: PNG, JPG, JPEG.")
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер файла не должен превышать 5 MB.")
        return image
