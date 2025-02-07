from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from products.models import Order, Product, ProductLike
from products.views import product_pagination
from django.db.models import Q
from django.core import serializers
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    request.session["authenticated"] = False
    request.session["show_overlay"] = False
    # return HttpResponse("Hello, world. You're at the home page.")
    return redirect('products:index')


# APIs here
def get_cart_total(request):
    order_id = request.session.get("order_id")
    order = Order.objects.get(pk=order_id)
    return JsonResponse({"no_distinct_items": order.order_distinct_amount})


def get_like_total(request):
    user_id = request.session.get("user_id")
    user = get_object_or_404(User, pk=user_id)

    # all ProductLike objects for the specific customer
    liked_products = ProductLike.objects.filter(customer=user.customer)
    # No of likes
    total_likes = liked_products.count()
    return JsonResponse({"no_distinct_items": total_likes})


def get_filtered_products(request, priceRange):
    # Define price range boundaries
    print(priceRange + " received by view")
    price_ranges = {
        "price-0": (0, 999999),
        "price-1": (0, 100),
        "price-2": (101, 300),
        "price-3": (301, 500),
        "price-4": (501, 1000),
        "price-5": (1001, 999999999),
    }

    search_string = request.GET.get("search_keyword")
    if search_string is None:
        search_string = ""

    # Get the price range for the selected option
    min_price, max_price = price_ranges.get(priceRange, (0, 99999999999))

    price_condition = Q(price__gte=min_price) & Q(price__lte=max_price)
    name_condition = Q(product_name__startswith=search_string) | Q(
        product_name__contains=search_string
    )
    combined_condition = price_condition & name_condition

    # Create a queryset to filter products within the specified price range
    filtered_products = Product.objects.filter(combined_condition)

    # Pagination
    filtered_products = product_pagination(request, filtered_products)
    number_list = list(range(1, 6))

    html_content = render(
        request,
        "products/marketplace_template.html",
        {"products": filtered_products, "number_list": number_list},
    )
    pagination_html = render(
        request, "products/pagination_template.html", {"products": filtered_products}
    )
    # Convert to JSON
    # data = serializers.serialize('json', filtered_products)
    return JsonResponse(
        {
            "updated_product_html": html_content.content.decode("utf-8"),
            "updated_pagination_html": pagination_html.content.decode("utf-8"),
        },
        safe=True,
    )


def reset_filtered_products(request):
    # Get all products
    products = Product.objects.all()
    products = product_pagination(request, products)
    number_list = list(range(1, 6))
    # Render template
    html_content = render(
        request,
        "products/marketplace_template.html",
        {"products": products, "number_list": number_list},
    )
    pagination_html = render(
        request, "products/pagination_template.html", {"products": products}
    )
    return JsonResponse(
        {
            "updated_product_html": html_content.content.decode("utf-8"),
            "updated_pagination_html": pagination_html.content.decode("utf-8"),
        },
        safe=True,
    )
