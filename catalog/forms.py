from django import forms

from .models import Product


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
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']

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
