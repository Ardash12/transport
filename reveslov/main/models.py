from django.db import models
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from ckeditor_uploader.fields import RichTextUploadingField


DELIVERI_FROM_CITY = [
    ('WD', 'От двери'),
    ('DW', 'Со склада'),

]

DELIVERI_TO_CITY = [
    ('WD', 'До двери'),
    ('DW', 'До склада'),
]

cash = 'CA'
non_cash = 'NO'

PAYMENT_METHOD = [
    (cash, 'Наличные'),
    (non_cash, 'Безналичные'),
]

fl = 'FL'
ul = 'UL'
ip = 'CL'

USER_TYPE = [
    (fl, 'Юридическое лицо'),
    (ul, 'Физическое лицо'),
    (ip, 'ИП'),
]

sender = 'SE'
receiver = 'RE'

PAYER= [
    (sender, 'Отправитель'),
    (receiver, 'Получатель'),
]

created = 'CR'
takeDoor = 'TA'
consignorsWarehouse = 'TO'
onWay = 'OW'
consigneesWarehouse = 'TD'
deliveryDoor = 'DD'
completed = 'CO'
canceled = 'CA'

STATUS_ORDER= [
    (created, 'Создан'),
    (takeDoor, 'Принят у отправителя'),
    (consignorsWarehouse, 'Готов к отправке'),
    (onWay, 'Осуществляется перевозка'),
    (consigneesWarehouse, 'Готов к доставке'),
    (deliveryDoor, 'Вышел на доставку'),
    (completed, 'Доставлен'),
]


class Client(models.Model):
    clientUser = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    surname = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    phone = models.CharField(max_length=100, blank=True, verbose_name='Телефон')
    address = models.CharField(max_length=250, blank=True, verbose_name='Адрес')
    companyName = models.CharField(max_length=250, blank=True, verbose_name='Название компании')
    inn = models.CharField(max_length=100, blank=True, verbose_name='ИНН')
    discount = models.FloatField(default=0, verbose_name='Скидка, %')
    status = models.CharField(max_length = 2, 
                        choices = USER_TYPE, 
                        default = ul,
                        verbose_name='Статус клиента')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.clientUser}'


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    cityDeparture = models.BooleanField(default=False, verbose_name='Является городом отправления')
    cityDestination = models.BooleanField(default=False, verbose_name='Является городом прибытия')
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class AdditionalServices(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    price = models.FloatField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Дополнительные услуги'
        verbose_name_plural = 'Дополнительные услуги'

    def __str__(self):
        return self.name


class NewFlatpage(models.Model):
    flatpage = models.OneToOneField(FlatPage, on_delete=models.CASCADE)
    description = RichTextUploadingField(verbose_name = 'Основной текстовый страницы', default='')

    def __str__(self):
        return self.flatpage.title

    class Meta:
        verbose_name = "Содержание страницы"
        verbose_name_plural = "Содержание страницы"


class ShippingRates(models.Model):
    fromTheCity = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='fromcity', 
        verbose_name='Город отправления'
        )
    toTheCity = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='tocity', 
        verbose_name='Город назначения'
        )
    rateUnder50 = models.FloatField(verbose_name='Масса <= 50 кг (фикс.стоимость)')
    rateUnder100 = models.FloatField(verbose_name='Масса <= 100 кг (за 1 кг)')
    rateUnder200 = models.FloatField(verbose_name='Масса <= 200 кг (за 1 кг)')
    rateUnder300 = models.FloatField(verbose_name='Масса <= 300 кг (за 1 кг)')
    rateUnder500 = models.FloatField(verbose_name='Масса <= 500 кг (за 1 кг)')
    rateUnder1000 = models.FloatField(verbose_name='Масса <= 1000 кг (за 1 кг)')
    rateOver1000 = models.FloatField(verbose_name='Масса > 1000 кг (за 1 кг)')

    def __str__(self):
        return f'{self.fromTheCity} - {self.toTheCity}'

    class Meta:
        verbose_name = "Тарифы на доставку"
        verbose_name_plural = "Тарифы на доставку"


class CityDeliveryRates(models.Model):
    city = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='city', 
        verbose_name='Город',
        unique=False,
        )
    rateUnder50 = models.FloatField(verbose_name='Масса <= 50 кг (фикс.стоимость)')
    rateUnder100 = models.FloatField(verbose_name='Масса <= 100 кг (за 1 кг)')
    rateUnder200 = models.FloatField(verbose_name='Масса <= 200 кг (за 1 кг)')
    rateUnder300 = models.FloatField(verbose_name='Масса <= 300 кг (за 1 кг)')
    rateUnder500 = models.FloatField(verbose_name='Масса <= 500 кг (за 1 кг)')
    rateUnder1000 = models.FloatField(verbose_name='Масса <= 1000 кг (за 1 кг)')
    rateOver1000 = models.FloatField(verbose_name='Масса > 1000 кг (за 1 кг)')

    def __str__(self):
        return f'{self.city}'

    class Meta:
        verbose_name = "Тарифы на доставку по городу"
        verbose_name_plural = "Тарифы на доставку по городу"


class DeliveryTime(models.Model):
    fromTheCity = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='fromcity_set', 
        verbose_name='Город отправления'
        )
    toTheCity = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='tocity_set', 
        verbose_name='Город назначения'
        )
    deliveryTime = models.IntegerField(verbose_name='Количество дней')

    def __str__(self):
        return f'{self.fromTheCity} / {self.toTheCity} / {self.deliveryTime}'

    class Meta:
        verbose_name = "Срок доставки"
        verbose_name_plural = "Срок доставки"


class Banner(models.Model):
    isActive = models.BooleanField(default=False, verbose_name='Показывать')
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to='%Y/%m/%d/')

    def __str__(self):
        if self.isActive:
            return f'{self.name} - Включён' 
        else: 
            return f'{self.name} - Выключен'

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class Insurance(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    rate = models.FloatField(verbose_name='Ставка, %/100 (Пример: 1% = 0,01)')
    priceMin = models.FloatField(verbose_name='Минимальная цена, руб.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страховка'
        verbose_name_plural = 'Страховка'

class Order(models.Model):
    fromCity = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='fromTheCity', 
        verbose_name='Город отправления'
        )
    deliveryFronCity = models.CharField(
        max_length = 2, 
        choices = DELIVERI_FROM_CITY, 
        default = 'DW',
        verbose_name='Сдать груз',
        )
    toCity = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        related_name='toTheCity', 
        verbose_name='Город назначения'
        )
    deliveryToCity = models.CharField(
        max_length = 2, 
        choices = DELIVERI_TO_CITY, 
        default = 'DW',
        verbose_name='Получить груз',
        )
    payer = models.CharField(
        max_length = 2, 
        choices = PAYER, 
        default = sender,
        verbose_name='Плательщик',
        )
    number = models.CharField(blank=True, max_length=100, verbose_name='Номер заказа для отслеживания')
    dateCreate = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')
    dateReceipt = models.DateField(blank=True, null=True, verbose_name='Дата приема груза')
    dateDelivery = models.DateField(blank=True, null=True, verbose_name='Дата получения груза')
    quantity = models.IntegerField(blank=True, null=True, verbose_name='Количество мест')
    weight = models.FloatField(verbose_name='Вес')
    volume = models.FloatField(verbose_name='Объем')
    insurance_sum = models.FloatField(default=0, verbose_name='Сумма страховки')
    discount = models.FloatField(default=0, verbose_name='Скидка')
    price = models.FloatField(blank=True, null=True, verbose_name='Итоговая сумма. (Рассчитывается при каждом сохранении заказа)')
    paymentMethod = models.CharField(
        max_length = 2, 
        choices = PAYMENT_METHOD, 
        default = non_cash,
        verbose_name='Способ оплаты'
        )
    status = models.CharField(
        max_length = 2, 
        choices = STATUS_ORDER, 
        default = created,
        verbose_name='Статус заказа',
        )
    senderName = models.CharField(blank=True, max_length = 100, verbose_name='Отправитель ФИО')
    senderEntity = models.CharField(blank=True, max_length = 100, verbose_name='Отправитель Юр.лицо')
    senderEmail = models.CharField(blank=True, max_length = 100, verbose_name='Отправитель E-mail')
    senderPhone = models.CharField(blank=True,max_length = 20, verbose_name='Отправитель телефон')
    senderAdds = models.CharField(blank=True, null=True, max_length = 150, verbose_name='Отправитель адрес')
    senderType = models.CharField(
        max_length = 2, 
        choices = USER_TYPE, 
        default = fl,
        verbose_name='Статус отправителя',
        )
    receiverName = models.CharField(blank=True, max_length = 100, verbose_name='Получатель ФИО')
    receiverEntity = models.CharField(blank=True, max_length = 100, verbose_name='Получатель Юр.лицо')
    receiverEmail = models.CharField(blank=True, max_length = 100, verbose_name='Получатель E-mail')
    receiverPhone = models.CharField(blank=True, max_length = 100, verbose_name='Получатель телефон')
    receiverAdds = models.CharField(blank=True, null=True, max_length = 100, verbose_name='Получатель адрес')
    receiverType = models.CharField(
        max_length = 2, 
        choices = USER_TYPE, 
        default = fl,
        verbose_name='Получатель статус',
        )
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='client', 
        verbose_name='Клиент',
        blank=True,
        null=True,
        )
    note = models.TextField(blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.number} / {self.fromCity} / {self.toCity}'


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    preview = models.TextField(max_length=120, verbose_name='Анонс')
    image = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    text = RichTextUploadingField(verbose_name = 'Текст')
    dateCreate = models.DateField(auto_now_add=True, verbose_name='Дата добавления новости')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Advantages(models.Model):
    number = models.IntegerField(unique=True, verbose_name='Номер преимущества')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return f'Преимущество №{self.number}'

    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'


class TextIndex(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    text = RichTextUploadingField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Текст для главной страницы'
        verbose_name_plural = 'Текст для главной страницы'
