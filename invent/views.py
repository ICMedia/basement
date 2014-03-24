from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import SingleObjectMixin
from invent.models import InventoryItem, InventoryItemPhoto

# Create your views here.

class ItemListView(ListView):
    model=InventoryItem
    template_name='index.html'
#    paginate_by=10
   
    def get_queryset(self):
        return InventoryItem.objects.filter(status='S').order_by("label_id")

class ItemView(DetailView):
    model=InventoryItem
    template_name='item_detail.html'
    slug_field='label_id'
