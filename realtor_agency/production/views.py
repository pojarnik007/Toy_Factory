from django.shortcuts import render
from .models import Toy, Order, Client, ToyType
from django.db.models import Sum, Count

def catalog(request):
    toys = Toy.objects.filter(is_active=True)
    toy_types = ToyType.objects.all()
    return render(request, 'catalog.html', {
        'toys': toys,
        'toy_types': toy_types
    })

def stats(request):
    top_toy = Order.objects.values('toy__name').annotate(total=Sum('quantity')).order_by('-total').first()
    bottom_toy = Order.objects.values('toy__name').annotate(total=Sum('quantity')).order_by('total').first()
    sales_by_type = Order.objects.values('toy__toy_type__name').annotate(total=Sum('quantity'))
    return render(request, 'stats.html', {
        'top_toy': top_toy,
        'bottom_toy': bottom_toy,
        'sales_by_type': sales_by_type
    })
