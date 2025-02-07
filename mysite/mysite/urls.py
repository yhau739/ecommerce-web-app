"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views  # import views.py from same app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("customers/", include("customers.urls")),
    # path("orders/", include("orders.urls")),
    path("products/", include("products.urls")),
    path("admin/", admin.site.urls),
    path("api/get_cart_total/", views.get_cart_total, name="get_cart_total"),
    path("api/get_like_total/", views.get_like_total, name="get_like_total"),
    path("api/get_filtered_products/<str:priceRange>", views.get_filtered_products, name="get_filtered_products"),
    path("api/reset_filtered_products/", views.reset_filtered_products, name="reset_filtered_products"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)