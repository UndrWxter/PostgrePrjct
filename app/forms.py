from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
        
class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={"class": "form-input"}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={"class": "form-input"}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        help_texts = {
            'username': 'Обязательное. 150 символов максимум. Только буквы, цифры и символы @/./+/-/_',
            'password1': 'Ваш пароль не должен быть слишком похож на другую вашу личную информацию и должен содержать как минимум 8 символов.',
        }

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Никнейм", widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))

from django import forms
from captcha.fields import CaptchaField
from .models import Contact

class ContactForm(forms.ModelForm):
    captcha = CaptchaField(label="Капча:", help_text="Введите текст с изображения")
    content = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        help_text="Введите ваше сообщение здесь."
    )

    class Meta:
        model = Contact
        fields = ["name", "email", "content"]
        labels = {
            "name": "Имя",
            "email": "Электронная почта",
        }
        help_texts = {
            "name": "Введите ваше имя",
            "email": "Введите ваш адрес электронной почты",
        }


    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit=commit)
        return instance
