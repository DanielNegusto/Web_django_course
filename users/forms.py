from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser


# Общий метод для обновления атрибутов
def update_widget_attrs(field, placeholder):
    field.widget.attrs.update({
        'class': 'form-control',
        'placeholder': placeholder
    })


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        label="Пароль"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        label="Подтверждение пароля"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 'avatar', 'phone_number', 'country']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'avatar': 'Аватар',
            'phone_number': 'Номер телефона',
            'country': 'Страна',
        }
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'avatar': forms.ClearableFileInput(),
            'phone_number': forms.TextInput(),
            'country': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обновление атрибутов для полей
        update_widget_attrs(self.fields['username'], 'Введите имя пользователя')
        update_widget_attrs(self.fields['email'], 'Введите адрес электронной почты')
        update_widget_attrs(self.fields['phone_number'], 'Введите номер телефона (необязательно)')
        update_widget_attrs(self.fields['country'], 'Введите страну (необязательно)')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Хешируем пароль
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'avatar', 'phone_number', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обновление атрибутов для полей
        update_widget_attrs(self.fields['email'], 'Введите ваш email')
        update_widget_attrs(self.fields['phone_number'], 'Введите номер телефона')
        update_widget_attrs(self.fields['country'], 'Введите страну')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and get_user_model().objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email
