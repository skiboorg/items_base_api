from django.contrib import admin

from .models import *

class ProductSupplyInline (admin.StackedInline):
    model = ProductSupply
    extra = 0

class ProductRemoveInline (admin.StackedInline):
    model = ProductRemove
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductSupplyInline,ProductRemoveInline]

class SubCategoryInline (admin.StackedInline):
    model = SubCategory
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = [SubCategoryInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(Izdelie)




