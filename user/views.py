from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordChangeForm

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('dashboard')  # Redireciona para a página principal após a alteração de senha

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.has_usable_password():
                login(request, user)
                return redirect('dashboard')  # Redireciona para a página principal após o login
            else:
                # Se a senha não for utilizável, redirecione para a página de alteração de senha
                return redirect('change_password')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')
