from django.contrib import admin
from ecomapp.models import Category,  Product, CartItem, Cart, Order, Image,Comment, Member,Chat, Messages
from django.urls import reverse

class InlineImage(admin.TabularInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineImage]

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status','date']
    list_display = ['id',
    # 'link_to_Cart',
    'date', 'first_name', 'total', 'city','status','item',]
    # def link_to_Cart(self, obj):
    #     link=reverse('admin:%s_%s_change' % (obj._meta.app_label,  'cart'),  args=[obj.item.id]) #model name has to be lowercase
    #     return u'<a href="%s">%s</a>' % (link,obj.item.id)
    # link_to_Cart.allow_tags=True



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