from django.contrib import admin
from .models import CustomUser, Product, DesignRequest

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_by', 'created_at')

class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('product', 'designer', 'status', 'created_at')

admin.site.register(CustomUser)
admin.site.register(Product, ProductAdmin)
admin.site.register(DesignRequest, DesignRequestAdmin)
