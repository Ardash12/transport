from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexPage.as_view(), name='home'),
    # path('calc/', views.IndexPage.as_view(), name='calc'),
    path('order_create/', views.order_create, name='order_create'),
    path('order_detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('search/', views.Search.as_view(), name='search'),
    # path('lk/', views.AccountIndex.as_view(), name='lk'),
    path('order_list/', views.OrderList.as_view(), name='order_list'),
    path('news_list/', views.NewsList.as_view(), name='news_list'),
    path('news_detail/<int:pk>/', views.NewsDetail.as_view(), name='news_detail'),
    path('client/', views.AccountIndex.as_view(), name='lk'),
    path('client/update/', views.client_update, name='client_update'),
]
