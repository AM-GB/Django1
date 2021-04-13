from django.urls import path

import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='index'),
    path('create/', ordersapp.OrderCreate.as_view(), name='create'),
    path('read/<int:pk>/', ordersapp.OrderDetail.as_view(), name='read'),
    path('update/<int:pk>/', ordersapp.OrderUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='delete'),

    path('complete/<int:pk>/', ordersapp.forming_complete, name='complete'),
]
