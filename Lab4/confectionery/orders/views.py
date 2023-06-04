from datetime import date

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Sum
from django.forms import modelformset_factory, formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from customers.models import Customer


class CreateOrderView(View):
    def get(self, request):
        OrderItemFormSet = formset_factory(OrderItemForm, extra=1)
        form = OrderForm(initial={'sale_date': date.today()})
        formset = OrderItemFormSet(prefix='orderitem')

        return render(request, 'create_order.html', {'form': form, 'formset': formset})

    def post(self, request):
        OrderItemFormSet = formset_factory(OrderItemForm, extra=1)
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, prefix='orderitem')

        if form.is_valid() and formset.is_valid():

            order = form.save(commit=False)
            order.sale_date = date.today()
            order.customer = get_object_or_404(Customer, username=request.user)
            order.save()

            for form in formset:
                item = form.save(commit=False)
                item.order = order
                item.price = item.quantity * item.product.price
                item.save()

            return redirect(reverse('order_detail', kwargs={'order_id': order.pk}))

        return render(request, 'create_order.html', {'form': form, 'formset': formset})


class OrderDetailView(View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        return render(request, 'order_detail.html', {'order': order})


class LatestOrdersView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        latest_orders = Order.objects.annotate(total_price=Sum('orderitem__price')).order_by('-id')[:10]
        return render(request, 'latest_orders.html', {'latest_orders': latest_orders})


class UpdateOrderItemPriceView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    def post(self, request, order_item_id):
        order_item = get_object_or_404(OrderItem, pk=order_item_id)
        new_price = request.POST.get('price')
        order_item.price = new_price
        order_item.save()
        return redirect('order_detail', order_id=order_item.order.id)

class MyOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        customer = get_object_or_404(Customer, username=request.user)
        orders = Order.objects.filter(customer=customer)
        return render(request, 'my_orders.html', {'orders': orders})