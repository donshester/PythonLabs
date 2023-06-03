from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product
from .forms import ProductForm


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ProductList(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products/product_list.html', {'products': products})


class ProductCreate(StaffRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'products/product_create.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'products/product_create.html', {'form': form})


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
