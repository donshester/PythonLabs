from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'product_create.html'
    fields = '__all__'
    permission_required = 'app.add_product'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_update.html'
    fields = '__all__'
    permission_required = 'app.change_product'


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product-list')
    permission_required = 'app.delete_product'