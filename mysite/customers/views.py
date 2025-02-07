from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from .models import Customer
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from products.views import clear_show_overlay
from products.models import ProductLike


def login(request):
    clear_show_overlay(request)
    return render(request, "customers/login.html")


def logout(request):
    request.session.flush()
    url = reverse("products:index") + "?show_logout_toast=true"
    return HttpResponseRedirect(url)


def login_request(request):
    # if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        # get user data from form
        user = form.get_user()
        try:
            auth_login(request, user)
        except:
            print("auth user failed")
        else:
            # Store custom session data (if needed)
            request.session["user_id"] = user.id
            request.session["authenticated"] = True

            url = reverse("products:index") + "?show_login_toast=true"

            # return HttpResponseRedirect(reverse("products:index"))
            return HttpResponseRedirect(url)
    else:
        return render(
            request,
            "customers/login.html",
            {
                "validation": True
            },
        )


def signup(request):
    clear_show_overlay(request)
    return render(request, "customers/signup.html")


def signup_request(request):
    if request.method == "POST":
        # Get user input from the form
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Create a new User instance
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        # Create a new Customer instance
        customer = Customer(user=user)
        customer.save()

        # Log in the user
        user = authenticate(username=username, password=password)
        auth_login(request, user)

        request.session["user_id"] = user.id
        request.session["authenticated"] = True

        # Redirect to a success page or the user's profile
        return HttpResponseRedirect(reverse("products:index"))

    return render(
        request,
        "signup.html",
        {
            "validation": True
        },
    )


def bookmarked(request):
    authenticated = request.session.get("authenticated")
    user_id = request.session.get("user_id")
    print(user_id)
    # No list used for rating loop
    number_list = list(range(1, 6))
    user = get_object_or_404(User, pk=user_id)
    # all ProductLike objects for the specific customer
    liked_products = ProductLike.objects.filter(customer=user.customer)
    # Extract the liked products from the ProductLike objects
    liked_product_list = [product_like.product for product_like in liked_products]
    return render(
        request, "customers/bookmarked.html", {"products": liked_product_list, "number_list":number_list, "authenticated":authenticated}
    )


# Create your methods views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    latest_customer_list = Customer.objects.order_by("-created_at")[:5]
    # template = loader.get_template("customers/index.html")
    if latest_customer_list:
        # If there are customers in the list, render them
        context = {
            "latest_customer_list": latest_customer_list,
        }
        return render(request, "customers/index.html", context)
    else:
        # If there are no customers, render a message
        message = "No customers available."
        context = {
            "message": message,
        }
        return render(request, "customers/index.html", context)
