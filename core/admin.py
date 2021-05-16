from django.contrib import admin

# Register your models here.
from django.contrib import admin

from core import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Customer)
admin.site.register(models.FoodVenue)
admin.site.register(models.Item)
admin.site.register(models.Review)
admin.site.register(models.favorite_item)