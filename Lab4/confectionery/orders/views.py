from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Order
from .forms import OrderForm, OrderItemFormSet
from customers.models import Customer


class CreateOrderView(View):
    def get(self, request, product_id=None):
        form = OrderForm(initial={'sale_date': date.today()})
        formset = OrderItemFormSet(prefix='orderitem')

        if product_id:
            formset.initial = [{'product': product_id}]

        return render(request, 'create_order.html', {'form': form, 'formset': formset})

    def post(self, request):
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, prefix='orderitem')

        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.sale_date = date.today()
            order.customer = get_object_or_404(Customer, username=request.user)
            order.save()

            formset.instance = order

            for form in formset:
                item = form.save(commit=False)
                item.order = order
                item.save()

            return redirect(reverse('order_detail', kwargs={'order_id': order.pk}))

        return render(request, 'create_order.html', {'form': form, 'formset': formset})


class OrderDetailView(View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        return render(request, 'order_detail.html', {'order': order})



