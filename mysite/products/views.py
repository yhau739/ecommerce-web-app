from django.shortcuts import render
from .models import (
    Category,
    Product,
    Order,
    InsufficientStockError,
    OrderItem,
    ProductLike,
)
from django.db.models import Avg
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.db.models import Q
from customers.models import Customer

# Create your views here.
def index(request):
    # Session data
    authenticated = request.session.get("authenticated")
    show_overlay = request.session.get("show_overlay")

    # UI prompts
    show_login_toast = request.GET.get("show_login_toast") == "true"
    show_logout_toast = request.GET.get("show_logout_toast") == "true"

    if authenticated:
        # Setup session
        setup_session(request)

    # Get all categories
    categories = Category.objects.all()
    # No list used for rating loop
    number_list = list(range(1, 6))
    # Calculate the average rating for each product and annotate it to the queryset
    products_with_avg_ratings = Product.objects.annotate(
        avg_rating=ExpressionWrapper(
            Cast(Avg("rating__rating"), FloatField()), output_field=FloatField()
        )
    )
    top_rated_products = products_with_avg_ratings.order_by("-avg_rating")[:8]
    return render(
        request,
        "products/index.html",
        {
            "categories": categories,
            "products": top_rated_products,
            "number_list": number_list,
            "authenticated": authenticated,
            "show_overlay": show_overlay,
            "show_login_toast": show_login_toast,
            "show_logout_toast": show_logout_toast,
        },
    )


def detail(request, product_id):
    clear_show_overlay(request)
    authenticated = request.session.get("authenticated")
    if authenticated:
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        categories = Category.objects.all()
        # No list used for rating loop
        number_list = list(range(1, 6))
        return render(
            request,
            "products/detail.html",
            {
                "categories": categories,
                "product": product,
                "authenticated": authenticated,
                "number_list": number_list,
            },
        )
    else:
        print("AT ELSE BLOCK")
        request.session["show_overlay"] = True
        return redirect("products:index")


def cart(request):
    authenticated = request.session.get("authenticated")
    user_id = request.session.get("user_id")
    user = get_object_or_404(User, pk=user_id)
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, pk=order_id)

    return render(
        request, "products/cart.html", {"order": order, "authenticated": authenticated}
    )


def edit_cart(request, product_id, updated_quantity):
    try:
        order_id = request.session.get("order_id")
        order = Order.objects.get(pk=order_id)
        product = Product.objects.get(pk=product_id)

        # Call class function
        order.edit_cart(product, updated_quantity)
        # Get updated price to reflect UI
        order_item = get_object_or_404(OrderItem, order=order, product=product)
        return JsonResponse(
            {
                "success": True,
                "item_total": order_item.item_total,
                "order_total": order.total_amount,
            }
        )
    except InsufficientStockError as e:
        # Change here
        product_name = str(e)
        item_message = product_name
        return JsonResponse({"success": False, "items": item_message})


def add_to_cart(request, product_id, quantity):
    try:
        # If new user then create new order
        order_id = request.session.get("order_id")
        print(order_id)

        # quantity to add to cart
        add_quantity = quantity
        print(add_quantity)

        # filter & get the chosen product/order
        product = Product.objects.get(pk=product_id)
        order = Order.objects.get(pk=order_id)

        # delete from cart if already in cart
        if product_exists_in_order(request, order, product):
            order.delete_orderitem_from_cart(product)
            return JsonResponse(
                {
                    "success": True,
                    "message": "Product is already in cart, removing from cart",
                }
            )

        order.add_to_cart(product, add_quantity)
        print("Finished add to cart op")
        order.save()
        return JsonResponse(
            {"success": True, "message": "Product Successfully added to cart"}
        )
    except InsufficientStockError as e:
        # Change here
        product_name = str(e)
        item_message = product_name
        return JsonResponse(
            {"success": False, "message": "Insufficient stock", "items": item_message}
        )
    except Order.DoesNotExist:
        return JsonResponse({"success": False, "message": "Order not found"})


def create_order_if_not_exists(request, user_id):
    # Retrieve the user object based on the user_id
    user = get_object_or_404(User, pk=user_id)

    # Check if the user has any orders
    if not user.customer.order_set.exists():
        try:
            # User has no orders, create a new order
            create_new_order(request, user)

        except IntegrityError as e:
            # Handle any IntegrityError exceptions, such as unique constraint violations
            print("Error creating Order:", str(e))
    else:
        # User has existing orders
        for order in user.customer.order_set.all():
            if order.paid == False:
                # Use Order that has not been paid yet
                request.session["order_id"] = order.pk
                # Break
                return None
            else:
                continue

        # Finished checking, existing orders are paid
        create_new_order(request, user)


def create_new_order(request, user):
    order = Order.objects.create(customer=user.customer)

    # You can set other fields for the order if needed
    order.total_amount = 0  # Set initial total amount
    order.paid = False  # Set initial paid status

    # Save into user's session
    request.session["order_id"] = order.pk

    # Save the order
    order.save()


def marketplace(request):
    clear_show_overlay(request)
    authenticated = request.session.get("authenticated")
    category_filter = request.GET.get("category")

    if authenticated:
        # No list used for rating loop
        number_list = list(range(1, 6))

        # For filter through category
        if category_filter is not None:
            products = Product.objects.filter(categories__name=category_filter)
            products_page = product_pagination(request, products)
            return render(
                request,
                "products/marketplace.html",
                {"products": products_page, "number_list": number_list},
            )

        # For Search Requests
        # search_string = request.GET.get("search_keyword")
        # if search_string is not None:
        #     products = Product.objects.filter(
        #         Q(product_name__startswith=search_string)
        #         | Q(product_name__contains=search_string)
        #     )
        #     return render(
        #         request,
        #         "products/marketplace.html",
        #         {"products": products, "number_list": number_list},
        #     )

        products = Product.objects.all()
        products_page = product_pagination(request, products)

        return render(
            request,
            "products/marketplace.html",
            {
                "products": products_page,
                "number_list": number_list,
                "authenticated": authenticated,
            },
        )
    else:
        request.session["show_overlay"] = True
        return redirect("products:index")


def create_product_like(request, product_id):
    user_id = request.session.get("user_id")
    user = get_object_or_404(User, pk=user_id)
    product = get_object_or_404(Product, pk=product_id)
    # Check if like exist
    existing_like = check_existing_product_like(request, user, product)

    if existing_like:
        existing_like.delete()
        return JsonResponse({"message": "Product removed from bookmarked"})
    # New likes
    else:
        # Create
        product_like = ProductLike(customer=user.customer, product=product)
        product_like.save()
        return JsonResponse({"message": "Product Successfully bookmarked"})

def checkout_cart(request):
    # Sleep for UI
    import time
    time.sleep(3)

    if request.method == 'POST':
        # If new user then create new order
        order_id = request.session.get("order_id")
        order = Order.objects.get(pk=order_id)
        print(order_id)
        # 1. Mark order as paid
        # order.mark_as_paid()

        # 2. Update order_id at session
        # 2.1 Create new order for user + attach to session
        # user_id = request.session.get("user_id")
        # create_order_if_not_exists(request, user_id)

        total_amount = request.POST.get('total_amount')
        print(total_amount)

        # 3. Redirect to Order History Page
        # url = reverse("products:index") + "?show_login_toast=true"

        return HttpResponseRedirect(reverse("products:order"))


def order(request):
    authenticated = request.session.get("authenticated")
    if authenticated:
        user_id = request.session.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        customer = Customer.objects.get(user=user)

        # Filter and get all paid orders by customer
        paid_orders = Order.objects.filter(paid=True, customer=customer)

        # context = {
        #     'paid_orders': paid_orders
        # }

        return render(
            request, "products/order.html", {"paid_orders": paid_orders, "authenticated": authenticated}
        )
    else:
        request.session["show_overlay"] = True
        return redirect("products:index")

def check_existing_product_like(request, user, productObj):
    # Check if the user has already liked the product (if you want to prevent multiple likes)
    return ProductLike.objects.filter(customer__user=user, product=productObj).first()


def product_exists_in_order(request, orderObj, productObj):
    return OrderItem.objects.filter(order=orderObj, product=productObj).exists()


def setup_session(request):
    user_id = request.session.get("user_id")

    # Setup Shopping Cart
    create_order_if_not_exists(request, user_id)


def clear_show_overlay(request):
    if request.session.get("show_overlay"):
        del request.session["show_overlay"]


# Convert input into pagination objects
def product_pagination(request, products):
    # Pagination
    products_per_page = 3
    paginator = Paginator(products, products_per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
