from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LogoutView as DjangoLogoutView, LoginView as DjangoLoginView
from customers.models import Customer
from django.contrib.auth.models import Group
from customers.forms import ExtendedUserCreationForm


class CreateUser(View):
    def get(self, request):
        form = ExtendedUserCreationForm()
        return render(request, 'registration/create_user.html', {'form': form})

    def post(self, request):
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()

            customer = Customer.objects.create(
                email=user.email,
                first_name=form.cleaned_data.get('first_name'),
                second_name=form.cleaned_data.get('second_name'),
                phone=form.cleaned_data.get('phone'),
                date_of_birth=form.cleaned_data.get('date_of_birth'),
                username=user.username
            )

            customer_group = Group.objects.get(name='Customer')
            customer.groups.add(customer_group)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('product_list')
        else:
            return render(request, 'registration/create_user.html', {'form': form})


class LogoutView(DjangoLogoutView):
    next_page = 'product_list'


class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        redirect_to = self.request.GET.get('next', 'product_list')
        self.request.session.set_expiry(0)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return redirect(redirect_to)
