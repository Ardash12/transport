from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import (
    filter_users_by_email,
    get_user_model,
    perform_login,
    setup_user_email,
    sync_user_email_addresses,
    url_str_to_user_pk,
    user_email,
    user_pk_to_url_str,
    user_username,
)
from allauth.account import app_settings


from .models import (
    City, 
    Client, 
    DELIVERI_FROM_CITY,
    DELIVERI_TO_CITY,
    USER_TYPE,
    PAYER,
    PAYMENT_METHOD,
    )


class CalcForm(forms.Form):
    from_city = forms.ModelChoiceField(
        label=u'Город отправления',
        # initial=1,
        queryset=City.objects.filter(cityDeparture=True),
        widget=forms.Select,
    )
    to_city = forms.ModelChoiceField(
        label=u'Город назначения', 
        queryset=City.objects.filter(cityDestination=True)
    )
    weight = forms.FloatField(label=u'Вес, кг')
    volume = forms.FloatField(label=u'Объем, куб.м.')
    insurance = forms.IntegerField(label=u'Сумма страховки')
    # delivery_from_city = forms.CharField(
    #     label=u'Сдать груз',
    #     max_length=2,
    #     initial='DW',
    #     widget=forms.RadioSelect(attrs={'class': 'radio'}, choices=DELIVERI_FROM_CITY),
    # )
    delivery_from_city= forms.ChoiceField(widget=forms.RadioSelect, initial='DW', choices=DELIVERI_FROM_CITY)
    delivery_to_city= forms.ChoiceField(widget=forms.RadioSelect, initial='DW', choices=DELIVERI_TO_CITY)
    # delivery_to_city = forms.CharField(
    #     label=u'Получить груз',
    #     max_length=2,
    #     initial='DW',
    #     widget=forms.RadioSelect(choices=DELIVERI_TO_CITY),
    # )


class OrderForm(forms.Form):
    '''Форма заказа'''
    from_city = forms.ModelChoiceField(
        label=u'Город отправления', 
        queryset=City.objects.filter(cityDeparture=True)
    )
    to_city = forms.ModelChoiceField(
        label=u'Город назначения', 
        queryset=City.objects.filter(cityDestination=True)
    )
    weight = forms.FloatField(label=u'Вес, кг')
    volume = forms.FloatField(label=u'Объем, куб.м.')
    insurance = forms.FloatField(label=u'Сумма страховки')

    # отправитель
    sender_type = forms.CharField(
        label=u'Статус отправителя',
        max_length=2,
        initial='UL',
        widget=forms.RadioSelect(choices=USER_TYPE),
    )
    sender_name = forms.CharField(required=False, label=u'ФИО отправителя')
    sender_entity = forms.CharField(required=False, label=u'Юр.лицо отправителя')
    sender_phone = forms.CharField(required=False, label=u'Телефон отправителя')
    sender_email = forms.CharField(required=False, label=u'E-mail отправителя')
    delivery_from_city = forms.CharField(
        label=u'Сдать груз',
        max_length=2,
        initial='DW',
        widget=forms.RadioSelect(choices=DELIVERI_FROM_CITY),
    )
    sender_adds = forms.CharField(required=False, label=u'Адрес отправителя')
    # получатель
    receiver_type = forms.CharField(
        label=u'Статус отправителя',
        max_length=2,
        initial='UL',
        widget=forms.RadioSelect(choices=USER_TYPE),
    )
    receiver_name = forms.CharField(required=False, label=u'ФИО получателя')
    receiver_entity = forms.CharField(required=False, label=u'Юр.лицо получателя')

    receiver_phone = forms.CharField(label=u'Телефон получателя')
    receiver_email = forms.CharField(required=False, label=u'E-mail получателя')
    delivery_to_city = forms.CharField(
        label=u'Получить груз',
        max_length=2,
        initial='DW',
        widget=forms.RadioSelect(choices=DELIVERI_TO_CITY),
    )
    receiver_adds = forms.CharField(required=False, label=u'Адрес получателя')
    payer = forms.CharField(
        label=u'Плательщик',
        max_length=2,
        initial='SE',
        widget=forms.RadioSelect(choices=PAYER),
    )
    payment_method = forms.CharField(
        label=u'Способ оплаты',
        max_length = 2,
        initial='CA',
        widget=forms.RadioSelect(choices=PAYMENT_METHOD),
        )
    note = forms.CharField(max_length=300, required=False, label=u'Примечание')


class ClientSignupForm(SignupForm):
    '''Создаем Client при регистрации User'''

    def save(self, request):
        user = super(ClientSignupForm, self).save(request)
        user.save()
        client = Client(clientUser=user)
        client.save()
        return user
    
    def clean(self):
        super(SignupForm, self).clean()

        # `password` cannot be of type `SetPasswordField`, as we don't
        # have a `User` yet. So, let's populate a dummy user to be used
        # for password validation.
        User = get_user_model()
        dummy_user = User()
        user_username(dummy_user, self.cleaned_data.get("username"))
        user_email(dummy_user, self.cleaned_data.get("email"))
        password = self.cleaned_data.get("password1")
        if password:
            try:
                get_adapter().clean_password(password, user=dummy_user)
            except forms.ValidationError as e:
                self.add_error("password1", e)

        if (
            app_settings.SIGNUP_PASSWORD_ENTER_TWICE
            and "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    _("Пароли должны совпадать."),
                )
        return self.cleaned_data



    

class NewLoginForm(LoginForm):
    error_messages = {
        "account_inactive": "Этот аккаунт заблокирован",
        "email_password_mismatch": "Неверный email или пароль",
        "username_password_mismatch": "Неверный логин или пароль",
    }

    def login(self, *args, **kwargs):
        # Add your own processing here.
        # You must return the original result.
        return super(NewLoginForm, self).login(*args, **kwargs)


class NewResetPasswordForm(ResetPasswordForm):

    def clean_email(self):
        
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        if not self.users and not app_settings.PREVENT_ENUMERATION:
            raise forms.ValidationError(
                _("222222222222222222The e-mail address is not assigned to any user account")
            )
        return super(NewResetPasswordForm, self).clean_email()

    
class ClientUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'surname',
            'name',
            'patronymic',
            'phone',
            'address',
            'companyName',
            'status',
        ]
    
