import pprint
from datetime import datetime, timedelta, date
from statistics import mode, median, mean

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.http import HttpResponseBadRequest
from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
import os
from customers.models import Customer
from orders.models import Order

from products.models import Product


@login_required
@user_passes_test(lambda u: u.is_staff)
def statistics_view(request):
    customers = Customer.objects.annotate(total_purchases=Sum('order__orderitem__price')).exclude(
        total_purchases=None).order_by('-total_purchases')[:10]

    total_sales = [customer.total_purchases for customer in customers]
    average_sales = mean(total_sales) if total_sales else None
    sales_mode = mode(total_sales) if total_sales else None
    sales_median = median(total_sales) if total_sales else None

    ages = [customer.get_age() for customer in customers]
    average_age = mean(ages) if ages else None
    median_age = median(ages) if ages else None

    popular_product_type = Product.objects.values('category__name').annotate(
        count=Coalesce(Sum('order__orderitem__quantity'), 0)
    ).order_by('-count').first()

    profitable_product_type = Product.objects.values('category__name').annotate(
        total_revenue=Coalesce(Sum('order__orderitem__price'), 0)
    ).order_by('-total_revenue').first()
    today = date.today()
    return render(request, 'statistics.html', {
        'customers': customers,
        'average_sales': average_sales,
        'sales_mode': sales_mode,
        'sales_median': sales_median,
        'average_age': average_age,
        'median_age': median_age,
        'popular_product_type': popular_product_type['category__name'],
        'profitable_product_type': profitable_product_type['category__name'],
        'today': today,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def order_count_graph_view(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
        except ValueError:
            return HttpResponseBadRequest("Invalid date format")
        today = datetime.today()
        current_year = today.year

        if end_date <= start_date or start_date.year < current_year or end_date > today:
            return HttpResponseBadRequest("Invalid date range")

        dates = []
        counts = []
        current_date = start_date
        while current_date < end_date:
            next_date = current_date + timedelta(days=1)
            count = Order.objects.filter(sale_date__gte=current_date, sale_date__lt=next_date).count()
            dates.append(current_date)
            counts.append(count)
            current_date = next_date
        save_dir = os.path.join(settings.BASE_DIR, 'static')
        save_path = os.path.join(save_dir+'/images', 'order_count_graph.png')
        print(save_path)
        plt.plot(dates, counts)
        plt.xlabel('Date')
        plt.ylabel('Order Count')
        plt.title('Order Count Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

        return render(request, 'order_count_graph.html')

    return render(request, 'select_date_range.html')
