from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from orders.forms import OrderItemForm, OrderForm
from products.models import Product
from orders.models import OrderItem
from customers.models import Customer
class CartView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return not self.request.user.is_superuser

    def get(self, request):
        cart = request.session.get('cart', {})
        order_item_forms = []
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            form = OrderItemForm(initial={'product': product, 'quantity': quantity})
            order_item_forms.append(form)
        for form in order_item_forms:
            form.fields['product'].widget.attrs['disabled'] = True
            form.fields['quantity'].widget.attrs['disabled'] = True
        order_form = OrderForm()

        return render(request, 'cart.html', {'order_item_forms': order_item_forms, 'order_form': order_form})

    def post(self, request):
        cart = request.session.get('cart', {})
        order_item_forms = []
        order_form = OrderForm(request.POST)

        if 'delete' in request.POST:
            product_id = request.POST.get('delete')
            print(request.POST)
            if product_id in cart:
                del cart[product_id]
            request.session['cart'] = cart
            return redirect('cart')

        if order_form.is_valid():
            order = order_form.save(commit=False)
            customer = Customer.objects.get(username=request.user)
            order.customer = customer
            order.sale_date = date.today()
            order.save()

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                order_item = OrderItem(order=order, product=product, quantity=quantity)
                order_item.price = product.price * quantity
                order_item.save()

                product.quantity -= quantity
                product.save()

            del request.session['cart']
            return redirect('order_detail', order_id=order.pk)

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            form = OrderItemForm(initial={'product': product, 'quantity': quantity})
            order_item_forms.append(form)

        request.session['cart'] = cart

        return render(request, 'cart.html', {'order_item_forms': order_item_forms, 'order_form': order_form})

