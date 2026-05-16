from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.static import serve
import os

urlpatterns = [
    # -------------------------
    # React routes
    # -------------------------
    path('', TemplateView.as_view(template_name="index.html")),  # React homepage
    path('login/', TemplateView.as_view(template_name="index.html")),  # React login page
    path('register/', TemplateView.as_view(template_name="index.html")),

    # -------------------------
    # Django app routes (mounted under /djangoapp/)
    # -------------------------
    path('djangoapp/', include('djangoapp.urls')),

    # -------------------------
    # Admin and contact
    # -------------------------
    path('admin/', admin.site.urls),
    path('contact/', TemplateView.as_view(template_name="djangoapp/Contact.html")),

    # -------------------------
    # Authentication routes
    # -------------------------
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # -------------------------
    # Explicitly serve manifest and favicon
    # -------------------------
    path('manifest.json', serve, {
        'path': 'manifest.json',
        'document_root': os.path.join(settings.BASE_DIR, 'frontend/build')
    }),
    path('favicon.ico', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(settings.BASE_DIR, 'frontend/build')
    }),
]

# Static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
