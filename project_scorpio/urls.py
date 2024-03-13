from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from user.views import CustomPasswordChangeView, dashboard_view
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),  # Redireciona para a página de login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

