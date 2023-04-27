import logging

from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import CalcForm, OrderForm, ClientUpdateModelForm
from .calculator import calculator
from .models import (
    Banner, 
    City, 
    Insurance, 
    ShippingRates, 
    Client, 
    CityDeliveryRates, 
    Order, 
    DeliveryTime, 
    News, 
    Advantages,
    TextIndex,
    )


logger = logging.getLogger(__name__)


class IndexPage(TemplateView):
    '''Главная страница'''
    template_name = 'index.html'
    
    @property
    def advantages(self) -> dict:
        # Преимущества
        adv_all = Advantages.objects.all()
        advantages = {
            'a1': adv_all.get(number=1),
            'a2': adv_all.get(number=2),
            'a3': adv_all.get(number=3),
            'a4': adv_all.get(number=4),
            'a5': adv_all.get(number=5),
            'a6': adv_all.get(number=6),
        }
        return advantages

    def get_context_data(self, **kwargs):
        result, form = calculator(self.request)
        context = super().get_context_data(**kwargs)
        context['form'] = form
        context['result'] = result
        context['banner'] = Banner.objects.filter(isActive=True).first()
        context['advantages'] = self.advantages
        context['text_index'] = TextIndex.objects.all().first()
        return context
    

def order_create(request):
    '''Создать заказ'''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                client = Client.objects.get(clientUser = request.user)
                discount = client.discount
            else:
                client = None
                discount = 0

            order = Order.objects.create(
                client = client,
                discount = discount,
                fromCity = form.cleaned_data['from_city'],
                toCity = form.cleaned_data['to_city'],
                weight = form.cleaned_data['weight'],
                volume = form.cleaned_data['volume'],
                insurance_sum = form.cleaned_data['insurance'],
                deliveryFronCity = form.cleaned_data['delivery_from_city'],
                senderAdds = form.cleaned_data['sender_adds'],
                deliveryToCity = form.cleaned_data['delivery_to_city'],
                receiverAdds = form.cleaned_data['receiver_adds'],
                senderName = form.cleaned_data['sender_name'],
                senderType = form.cleaned_data['sender_type'],
                senderPhone = form.cleaned_data['sender_phone'],
                senderEmail = form.cleaned_data['sender_email'],
                senderEntity = form.cleaned_data['sender_entity'],
                receiverType = form.cleaned_data['receiver_type'],
                receiverName = form.cleaned_data['receiver_name'],
                receiverPhone = form.cleaned_data['receiver_phone'],
                receiverEmail = form.cleaned_data['receiver_email'],
                receiverEntity = form.cleaned_data['receiver_entity'],
                paymentMethod = form.cleaned_data['payment_method'],
                payer = form.cleaned_data['payer'],
                note = form.cleaned_data['note'],
                )
            order.number = f'UI0000{order.id}'
            order.save()
            return render(request, 'order_detail.html', {'order': order})
        
    elif request.method == 'GET':
        from_city = request.GET.get('from_city')
        to_city = request.GET.get('to_city')
        weight = request.GET.get('weight')
        volume = request.GET.get('volume')
        insurance = request.GET.get('insurance')
        form = OrderForm(initial={
            'from_city': from_city,
            'to_city': to_city,
            'weight': weight,
            'volume': volume,
            'insurance': insurance
            })
    return render(request, 'order_create.html', {'form': form})


@login_required
def order_detail(request, pk):
    '''Подробное описание заказа'''
    order = Order.objects.get(id=pk)
    return render(request, 'order_detail.html', {'order': order})


class Search(TemplateView):
    '''Страница поиска'''
    model = Order
    template_name = 'order_treking.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q')
        order = Order.objects.filter(number=query)
        if self.request.method == 'GET' and 'q' in self.request.GET and not order.exists():
            no_order = 'Заказ не найден.'
        else:
            no_order = 'Введите номер заказа для отслеживания.'
        order = Order.objects.filter(number=query)
        context = super().get_context_data(**kwargs)
        context['order'] = order.first()
        context['no_order'] = no_order
        context['query'] = query
        return context
  

class AccountIndex(LoginRequiredMixin, TemplateView):
    '''Личный кабинет'''
    template_name = 'personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_user'] = Client.objects.get(clientUser=self.request.user)
        return context
    


class OrderList(LoginRequiredMixin, ListView):
    '''Список заказов'''
    template_name = 'order_list.html'
    model = Order
    context_object_name = 'orders'
    paginate_by = 6
    
    def get_queryset(self):
        return Order.objects.filter(client__clientUser=self.request.user).order_by('-dateCreate')


@login_required
def client_update(request):
    '''Изменать данные клиента'''
    if request.method == 'GET':
        client = Client.objects.get(clientUser=request.user)
        form = ClientUpdateModelForm(initial={
            'name': client.name,
            'patronymic': client.patronymic,
            'surname': client.surname,
            'phone': client.phone,
            'address': client.address,
            'companyName':client.companyName,
            'status': client.status,
            })
        return render(request, 'client_update.html', {'form': form})
    elif request.method == 'POST':
        form = ClientUpdateModelForm(request.POST)
        if form.is_valid():
            client = Client.objects.update(
                name = form.cleaned_data['name'],
                patronymic = form.cleaned_data['patronymic'],
                surname = form.cleaned_data['surname'],
                phone = form.cleaned_data['phone'],
                address = form.cleaned_data['address'],
                companyName = form.cleaned_data['companyName'],
                status = form.cleaned_data['status'],
            )
        return redirect('lk')


class NewsList(ListView):
    '''Список новостей'''
    template_name = 'news_list.html'
    model = News
    queryset = News.objects.all()
    context_object_name = 'news_list'
    ordering = ['-dateCreate']
    paginate_by = 6


class NewsDetail(DetailView):
    '''Страница новости'''
    template_name = 'news_detail.html'
    model = News
    context_object_name = 'news'


