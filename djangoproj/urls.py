from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('contact/', TemplateView.as_view(template_name="djangoapp/Contact.html")),

    # Django admin
    path('admin/', admin.site.urls),

    # Mount your app at root
    path('', include('djangoapp.urls')),

    # Authentication routes
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
