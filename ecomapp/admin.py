from django.contrib import admin
from ecomapp.models import Category,  Product, CartItem, Cart, Order, Image,Comment, Member,Chat, Messages

class InlineImage(admin.TabularInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineImage]

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']



admin.site.register(Category)
# admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Comment)
admin.site.register(Member)
admin.site.register(Chat)
admin.site.register(Messages)


admin.site.register(Order, OrderAdmin)