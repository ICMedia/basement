from django.db import models

from django.contrib.auth import get_user_model
from django.utils.html import format_html
User = get_user_model()

class InventoryItem(models.Model):
    SOCIETIES = (
        ('J', 'Jazz and Rock'), 
        ('R', 'IC Radio'),
        ('F', 'Felix'),
        ('P', 'PhotoSoc'),
        ('S', 'STOIC'),
        ('M', 'Media'),
        ('O', 'Other or Unknown')
    )
    SELL_OPTIONS = (
        ('K', 'Keep'),
        ('D', 'Delay until budget finalised'),
        ('S', 'Sell'),
	('T', 'Techbid'),
	('B', 'Bin or give / sell')	
    )
    def number():
        no = InventoryItem.objects.count()
        if no == None:
            return 1
        else:
            return no + 1

    def __unicode__(self):
        return u"%d [WB-%d] %s (%s)" % (self.label_id, self.label_id, self.name, self.get_society_display())
    
    name = models.CharField(max_length=200)
    society = models.CharField(max_length=1, choices=SOCIETIES, default='M')
    status = models.CharField(max_length=1, choices=SELL_OPTIONS, default='K')
    description = models.CharField(max_length=2000, blank=True)
    label_id= models.IntegerField(('Label ID: WB-'), unique=True, max_length=6)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    addedby = models.ForeignKey(User)
    reserve = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#    storagelocation=models.CharField(max_length=1, choices=LOCATIONS)
    autobid_reached=models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True) 
    highestsealedbid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    biddernumber = models.IntegerField(blank=True, null=True)
    winningbiddernumber = models.IntegerField(blank=True, null=True)
    winningbidamount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    needsapproval = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    collected = models.BooleanField(default=False)

    parentid = models.ForeignKey("self", blank=True, null=True)

    def sold(self):
        return self.winningbidamount is not None
    sold.boolean = True

    def sold_to(self):
        if self.winningbiddernumber is None:
            return ''
        try:
            return Bidder.objects.get(number=self.winningbiddernumber)
        except Bidder.DoesNotExist:
            return '???'
    sold_to.admin_order_field = 'winningbiddernumber'

    def link_to_admin_for_sold_to(self):
        st = self.sold_to()
        if st == '' or st == '???':
            return st
        return format_html('<a href="/admin/invent/bidder/{0}/">{1}</a>', st.pk, st.name)
    link_to_admin_for_sold_to.short_description = 'Sold to'
    link_to_admin_for_sold_to.admin_order_field = 'winningbiddernumber'
    
    class Meta:
        ordering = ('-label_id',)
class InventoryItemRelationship(models.Model):
    parent_inventory_item = models.ForeignKey(InventoryItem, related_name="parent")
    child_inventory_item = models.ForeignKey(InventoryItem, related_name="children", unique=True)

class InventoryItemPhoto(models.Model):
    item = models.ForeignKey(InventoryItem, related_name='photos')
    image = models.ImageField(upload_to='inventory_photos')

class Bidder(models.Model):
    
    def gennumber():
        no = Bidder.objects.count()
        if no == None:
            return 1
        else:
            return no + 1

    name = models.CharField(max_length=100)
    number = models.IntegerField(max_length=10, default=gennumber)
    phone = models.CharField(max_length=100, blank=True, null=False, default='')
    email = models.CharField(max_length=300, blank=True, null=False, default='')
