from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RealEstateObjectForm
from .models import *
from users.decorators import role_required
from users.models import Position
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
 

def catalog(request):
    search_query = request.GET.get('q')
    selected_categories = request.GET.getlist('categories')
    sort_param = request.GET.get('sort')
    
    queryset = RealEstateObject.objects.filter(on_sale=True)
    
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    sorting_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'title_asc': 'title',
        'title_desc': '-title',
    }
    order_by = sorting_map.get(sort_param, 'pk')
    queryset = queryset.order_by(order_by)
    
    if selected_categories:
        queryset = queryset.filter(category__slug__in=selected_categories).distinct()
    
    all_categories = ObjectCategory.objects.all()
    
    return render(request, 'real_estate/catalog.html', {
        'real_estate': queryset,
        'all_categories': all_categories,
        'selected_categories': selected_categories,
        'search_query': search_query,
        'user': request.user
    })
 
@role_required([Position.ADMIN])
def create(request):
    if request.method == "POST":
        form = RealEstateObjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                real_estate_object = form.save()
                messages.success(request, 'Объект успешно создан!')
                return redirect("real_estate:edit", slug=real_estate_object.slug)
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = RealEstateObjectForm()

    return render(request, 'real_estate/create.html', {
        'form': form,
        'categories': ObjectCategory.objects.all()
    })

@role_required([Position.ADMIN])
def real_estate_detail(request, slug):
    obj = get_object_or_404(RealEstateObject, slug=slug)
    
    if request.method == 'POST':
        form = RealEstateObjectForm(
            request.POST, 
            request.FILES, 
            instance=obj
        )
        if form.is_valid():
            form.save()
            return redirect('real_estate:catalog')
    else:
        form = RealEstateObjectForm(instance=obj)
    
    return render(request, 'real_estate/edit.html', {
        'form': form,
        'object': obj
    })


@role_required([Position.ADMIN])
def delete(request, slug):
    obj = get_object_or_404(RealEstateObject, slug=slug)
    obj.delete()
    return redirect('real_estate:catalog')


from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import transaction

def detail(request, slug):
    obj = get_object_or_404(RealEstateObject, slug=slug) 
    return render(request, 'real_estate/detail.html', {'object': obj})


@role_required([Position.CLIENT])
def buy(request, slug):
    obj = get_object_or_404(RealEstateObject, slug=slug)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                obj.refresh_from_db()
                if not obj.on_sale:
                    messages.error(request, 'Объект уже продан')
                    return redirect('real_estate:detail', slug=slug)
                
                if not request.POST.get('confirm'):
                    messages.error(request, 'Подтвердите покупку')
                    return redirect('real_estate:detail', slug=slug)
                
                Sale.objects.create(
                    client=request.user,
                    real_estate_object=obj
                )
                obj.on_sale = False
                obj.save()
                
                messages.success(request, 'Покупка успешно завершена!')
                return redirect('real_estate:detail', slug=slug)
                
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
    
    return redirect('real_estate:detail', slug=slug)


@role_required([Position.ADMIN, Position.EMPLOYEE])
def sales(request):
    sales_list = Sale.objects.all()
    return render(request, 'real_estate/sales.html', context={'sales': sales_list, 'user': request.user})