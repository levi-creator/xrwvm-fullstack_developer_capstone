from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # API and backend endpoints
    path('manifest.json', views.manifest, name='manifest'),
    path('get_cars', views.get_cars, name='get_cars'),
    path('get_local_cars', views.get_local_cars, name='get_local_cars'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout, name='logout'),
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review', views.add_review, name='add_review'),

    # Optional legacy static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),

    # React entry point (must be last)
    path('', views.index, name='index'),
    re_path(r'^(?!djangoapp/).*$', views.index),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
