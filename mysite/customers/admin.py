from django.contrib import admin

# Register your models here.
# Make apps modifiable on admin

from .models import Customer

admin.site.register(Customer)