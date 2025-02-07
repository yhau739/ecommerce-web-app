from django.db import models
from customers.models import Customer
from django.db.models import Sum, Avg
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category_img = models.ImageField(default="", upload_to="category_images/")

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )  # Percentage discount
    stock_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        Category
    )  # Many-to-many relationship with categories
    product_img = models.ImageField(upload_to="product_images/")

    def calculate_average_rating(self):
        return Rating.objects.filter(product=self).aggregate(Avg("rating"))[
            "rating__avg"
        ]

    # def add_to_cart(self, quantity):
    #     insufficient_stock_items = []
    #     # Iterate through order items and update product quantities
    #     for order_item in self.orderitem_set.all():
    #         product = order_item.product
    #         if product.quantity >= order_item.quantity:
    #             product.quantity -= order_item.quantity
    #             product.save()
    #         else:
    #             # Handle insufficient product quantity here
    #             pass

    #     if insufficient_stock_items:
    #         # If there are insufficient stock items, raise an exception
    #         raise InsufficientStockError(insufficient_stock_items)

    # Computed properties
    @property
    def rating_count(self):
        return self.rating_set.count()

    @property
    def average_rating(self):
        avg_rating = self.calculate_average_rating()
        return avg_rating if avg_rating else 0

    @property
    def partial_rating(self):
        avg_rating = self.calculate_average_rating()
        decimal_part = avg_rating - int(avg_rating)  # Extract decimal part
        return int(decimal_part * 10) if decimal_part else 0

    @property
    def price_after_discount(self):
        return self.price * ((100 - self.discount) / 100)

    @property
    def has_discount(self):
        if self.price == self.price_after_discount:
            return False
        else:
            return True

    def __str__(self):
        return self.product_name


# Custom Exception Raised
class InsufficientStockError(Exception):
    pass


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )  # Use DecimalField for currency
    paid = models.BooleanField(default=False)

    def update_total_amount(self):
        # Calculate the total amount by summing the item totals from OrderItems
        total = self.orderitem_set.aggregate(Sum("item_total"))["item_total__sum"]
        self.total_amount = total if total is not None else 0

    def edit_cart(self, product, new_quantity):
        order_item = get_object_or_404(OrderItem, order=self, product=product)

        if new_quantity <= product.stock_quantity:
            order_item.quantity = new_quantity
            order_item.save()

            # Recalculate the total_amount for the order
            self.save()
        else:
            # If the requested quantity exceeds inventory, raise an exception
            raise InsufficientStockError(
                (f"Insufficient stock for product: {product.product_name}, only {product.stock_quantity} quantity were left!")
            )

    def add_to_cart(self, product, quantity):
        # Check if the requested quantity exceeds available inventory
        if product.stock_quantity >= quantity:
            # Create an OrderItem for the product and quantity
            order_item, created = OrderItem.objects.get_or_create(
                order=self, product=product, defaults={"quantity": quantity}
            )

            # If an OrderItem already existed, update the quantity
            if not created:
                order_item.quantity += quantity
                order_item.save()

            # # Deduct the quantity from the product's inventory
            # product.quantity -= quantity
            # product.save()

        else:
            # If the requested quantity exceeds inventory, raise an exception
            raise InsufficientStockError(
                (f"Insufficient stock for product: {product.product_name}, only {product.stock_quantity} quantity were left!")
            )

    def delete_orderitem_from_cart(self, product):
        try:
            order_item = self.orderitem_set.get(product=product)
            order_item.delete()
            # Deletion was successful
        except OrderItem.DoesNotExist:
            return False

    def mark_as_paid(self):
        if not self.paid:
            insufficient_stock_items = []
            # Iterate through order items and update product quantities
            for order_item in self.orderitem_set.all():
                product = order_item.product
                if product.stock_quantity >= order_item.quantity:
                    product.stock_quantity -= order_item.quantity
                    product.save()
                else:
                    insufficient_stock_items.append(order_item)

            if insufficient_stock_items:
                # If there are insufficient stock items, raise an exception
                raise InsufficientStockError(insufficient_stock_items)

            # Set the order_date and mark the order as paid
            self.order_date = timezone.now()
            self.paid = True
            self.save()
            # Inventory deduct by the ordered amount

    @property
    def order_total_amount(self):
        self.update_total_amount()
        return self.total_amount

    @property
    def order_distinct_amount(self):
        return self.orderitem_set.count()

    def save(self, *args, **kwargs):
        # Update the total amount before saving
        if self.pk is not None:
            self.update_total_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.pk} by {self.customer.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_total = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def calculate_item_total(self):
        if self.product:
            self.item_total = self.quantity * self.product.price
        else:
            self.item_total = 0

    # This will trigger when admin clicks save btn from admin panel
    def save(self, *args, **kwargs):
        self.calculate_item_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.product_name} ({self.quantity} units)"


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # at controller need to check what product was selected to prevent double rating
    # make sure product selected is inside ORDER
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # At UI need to make sure Order is paid b4 user can create rating Obj
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # ratings are on a scale of 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Order.customer.user.username} - {self.rating} star - {self.product.product_name}"


class ProductLike(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE
    )  # The user who liked the product
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # The product that was liked
    liked_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the like was created

    class Meta:
        unique_together = (
            "customer",
            "product",
        )  # Ensure a user can like a product only once

    def __str__(self):
        return f"{self.customer.user.username} liked {self.product.product_name}"
