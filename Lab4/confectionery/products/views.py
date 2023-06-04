from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Manufacturer, Category
from .forms import ProductForm
import requests


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProductList(View):
    def get(self, request):
        products = Product.objects.all()
        manufacturers = Manufacturer.objects.all()
        categories = Category.objects.all()

        manufacturer_id = request.GET.get('manufacturer')
        category_id = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        search_query = request.GET.get('search')

        if manufacturer_id:
            products = products.filter(manufacturer_id=manufacturer_id)

        if category_id:
            products = products.filter(category_id=category_id)

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        if search_query:
            products = products.filter(
                name__icontains=search_query
            )

        return render(request, 'products/product_list.html', {
            'products': products,
            'manufacturers': manufacturers,
            'categories': categories,
            'selected_manufacturer': int(manufacturer_id) if manufacturer_id else None,
            'selected_category': int(category_id) if category_id else None,
            'selected_min_price': float(min_price) if min_price else None,
            'selected_max_price': float(max_price) if max_price else None,
            'selected_search_query': search_query,
        })


class ProductCreate(StaffRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        joke = self.get_joke()
        return render(request, 'products/product_create.html', {'form': form, 'joke': joke})
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'products/product_create.html', {'form': form})

    def get_joke(self):
        response = requests.get('https://v2.jokeapi.dev/joke/Programming?type=single')
        if response.status_code == 200:
            data = response.json()
            joke = data['joke']
            return joke
        else:
            return None


class ProductDetail(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        return render(request, 'products/product_detail.html', {'product': product})


class ProductEdit(StaffRequiredMixin, View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        form = ProductForm(instance=product)
        return render(request, 'products/product_edit.html', {'product': product, 'form': form})

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'products/product_edit.html', {'product': product, 'form': form})


class ProductDelete(StaffRequiredMixin, View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        return render(request, 'products/product_delete.html', {'product': product})

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return redirect('product_list')
