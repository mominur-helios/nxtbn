from django.contrib import admin
from nxtbn.product.models import Category,Collection,Product, ProductVariant

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    readonly_fields = ('parent',)

admin.site.register(Category,CategoryAdmin)


class CollectionAdmin(admin.ModelAdmin):

    list_display = ('id','name', 'is_active', 'created_by', 'last_modified_by')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('last_modified_by',) 
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active', 'image')
        }),
        ('Metadata', {
            'fields': ('created_by', 'last_modified_by')
        })
    )


admin.site.register(Collection,CollectionAdmin)




class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    list_display = ('id','name', "slug", 'category', 'vendor', 'type', 'subscribable')
    list_filter = ('category', 'vendor', 'type', 'subscribable')
    search_fields = ('name', 'summary', 'description')
    readonly_fields = ('last_modified_by',) 

admin.site.register(Product, ProductAdmin)