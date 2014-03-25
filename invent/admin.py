from django.contrib import admin
from invent.models import InventoryItem, InventoryItemPhoto, Bidder, InventoryItemRelationship

# Register your models here.
# admin.site.register(InventoryItem)

class InventoryItemPhotoInline(admin.TabularInline):
    model = InventoryItemPhoto
    extra = 3

class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 10
    fields = ['label_id']
class InventoryItemRelationshipInline(admin.TabularInline):
    model = InventoryItemRelationship
    fk_name = "parent_inventory_item"
    extra = 10 
class InventoryItemSoldListFilter(admin.SimpleListFilter):
    title = u'sold'

    parameter_name = 'sold'

    def lookups(self, request, model_admin):
        return (
            ('y', 'Yes'),
            ('n', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'y':
            return queryset.exclude(winningbidamount=None)
        if self.value() == 'n':
            return queryset.filter(winningbidamount=None)

class InventoryItemAdmin(admin.ModelAdmin):
   # inlines = [ InventoryItemPhotoInline, InventoryItemRelationshipInline, InventoryItemInline ]
    inlines = [ InventoryItemPhotoInline, InventoryItemRelationshipInline,]
    list_display = ['label_id', 'name', 'society', 'status', 'collected', 'paid', 'sold', 'link_to_admin_for_sold_to', 'winningbidamount']
    search_fields = ['label_id', 'society', 'status']
    list_filter = ['collected', 'paid', InventoryItemSoldListFilter]
    list_editable = ['collected', 'paid', 'status']

class BidderAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']
admin.site.register(InventoryItem,InventoryItemAdmin)
admin.site.register(Bidder, BidderAdmin)
