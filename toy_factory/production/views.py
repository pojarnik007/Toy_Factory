from django.views.decorators.http import require_POST
from django.core.paginator import Paginator  # <--- ДОБАВЛЕН ИМПОРТ

from .forms import ToyForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Toy, ToyType, Order, Client, PickupPoint, Cart, CartItem
from users.models import Position
from users.decorators import role_required
from promotions.models import PromoCode
from django.utils import timezone


def catalog(request):
    search_query = request.GET.get('q')
    selected_types = request.GET.getlist('types')
    sort_param = request.GET.get('sort')

    queryset = Toy.objects.filter(is_active=True)

    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    sorting_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
    }
    order_by = sorting_map.get(sort_param, 'pk')
    queryset = queryset.order_by(order_by)

    if selected_types:
        queryset = queryset.filter(toy_type__id__in=selected_types).distinct()

    # === ЛОГИКА ПАГИНАЦИИ ===
    # Получаем количество элементов на странице из GET-запроса, по умолчанию 3
    per_page = request.GET.get('per_page', 3)
    try:
        per_page = int(per_page)
        if per_page < 1:
            per_page = 3
    except ValueError:
        per_page = 3

    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # ========================

    all_types = ToyType.objects.all()

    return render(request, 'production/catalog.html', {
        'toys': page_obj,      # Передаем страницу, чтобы цикл for работал по ней
        'page_obj': page_obj,  # Передаем объект страницы для навигации (номера страниц)
        'all_types': all_types,
        'selected_types': selected_types,
        'search_query': search_query,
    })


def toy_detail_view(request, pk):
    toy = get_object_or_404(Toy, pk=pk)
    return render(request, 'production/toy_detail.html', {'toy': toy})


@login_required
def buy(request, pk):
    toy = get_object_or_404(Toy, pk=pk)
    user = request.user
    client, created = Client.objects.get_or_create(
        user=user,
        defaults={
            "name": user.get_full_name() or user.username,
            "phone": user.phone or "",
            "city": user.city or "",
            "email": user.email or "",
            "is_wholesale": False,
        }
    )
    pickup_points = PickupPoint.objects.filter(active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        pickup_point_id = request.POST.get('pickup_point')
        promo_code_text = request.POST.get('promo_code', '').strip()
        promo = None
        discount = 0

        if promo_code_text:
            try:
                promo = PromoCode.objects.get(text=promo_code_text, state='active')
                discount = promo.discount_percent
            except PromoCode.DoesNotExist:
                promo = None
                discount = 0
                messages.warning(request, "Промокод не найден или неактивен.")

        pickup_point = get_object_or_404(PickupPoint, id=pickup_point_id, active=True)

        if quantity > toy.in_stock or quantity <= 0:
            messages.error(request, "Недостаточно товара в наличии.")
            return redirect('production:buy', pk=toy.pk)

        total_cost = toy.price * quantity
        discount_amount = total_cost * discount / 100
        final_cost = total_cost - discount_amount

        if 'confirm' in request.POST:
            order = Order.objects.create(
                client=client,
                toy=toy,
                quantity=quantity,
                status='created',
                pickup_point=pickup_point,
                promo_code=promo if promo else None,
            )
            toy.in_stock -= quantity
            toy.save()
            messages.success(request, f"Заказ оформлен! Итоговая сумма: {final_cost:.2f} ₽")
            return redirect('production:order_confirm', order_id=order.id)
        else:
            # показать страницу подтверждения
            return render(request, 'production/order_confirm.html', {
                'toy': toy,
                'quantity': quantity,
                'pickup_point': pickup_point,
                'total_cost': total_cost,
                'promo': promo,
                'discount': discount,
                'discount_amount': discount_amount,
                'final_cost': final_cost,
                'promo_code_text': promo_code_text,
            })

    return render(request, 'production/buy.html', {
        'toy': toy,
        'pickup_points': pickup_points,
    })


@login_required
def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id, client__user=request.user)
    return render(request, 'production/order_confirmed.html', {'order': order})


@role_required([Position.ADMIN])
def create(request):
    if request.method == "POST":
        form = ToyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                toy = form.save()
                messages.success(request, 'Игрушка успешно создана!')
                return redirect("production:edit", pk=toy.pk)
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = ToyForm()
    return render(request, 'production/create.html', {
        'form': form
    })


@role_required([Position.ADMIN])
def toy_detail(request, pk):
    toy = get_object_or_404(Toy, pk=pk)

    if request.method == 'POST':
        form = ToyForm(request.POST, instance=toy)
        if form.is_valid():
            form.save()
            return redirect('production:catalog')
    else:
        form = ToyForm(instance=toy)

    return render(request, 'production/edit.html', {
        'form': form,
        'toy': toy
    })


@role_required([Position.ADMIN])
def delete(request, pk):
    toy = get_object_or_404(Toy, pk=pk)
    toy.delete()
    return redirect('production:catalog')


@role_required([Position.ADMIN, Position.EMPLOYEE])
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'production/order_list.html', {'orders': orders})


@role_required([Position.ADMIN, Position.EMPLOYEE])
def order_confirm_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, 'Статус заказа обновлён.')
        return redirect('production:orders')
    return render(request, 'production/admin_order_confirm.html', {'order': order})


@require_POST
@login_required
def add_to_cart(request, toy_id):
    toy = get_object_or_404(Toy, id=toy_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, toy=toy)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("production:cart_view")


@require_POST
@login_required
def update_cart_item(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1
    elif action == "remove":
        item.delete()
        return redirect("production:cart_view")
    item.save()
    return redirect("production:cart_view")


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("toy").all()
    total = sum(item.total_price for item in items)
    return render(request, "production/cart.html", {
        "cart": cart,
        "items": items,
        "total": total
    })


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related("toy").all()

    if not items:
        messages.error(request, "Корзина пуста")
        return redirect("production:cart_view")

    total = sum(item.total_price for item in items)

    if request.method == "POST":
        # Тут можно интегрировать платёжку или просто оформить заказ
        messages.success(request, f"Оплата прошла успешно! Итоговая сумма: {total:.2f} ₽")
        # Очистка корзины после оплаты
        cart.items.all().delete()
        return redirect("production:catalog")

    return render(request, "production/checkout.html", {"cart": cart, "items": items, "total": total})