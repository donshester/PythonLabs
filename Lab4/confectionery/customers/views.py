from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LogoutView as DjangoLogoutView, LoginView as DjangoLoginView


class CreateUser(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/create_user.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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

