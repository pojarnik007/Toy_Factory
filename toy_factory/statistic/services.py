from django.db.models import Sum, F
from statistics import mean, median, mode, StatisticsError
from production.models import Order, ToyType
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def get_base64_plot():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.clf()
    return base64.b64encode(image_png).decode('utf-8')

def get_client_sales_chart():
    client_sales = (
        Order.objects
        .select_related("client")
        .values("client__name")
        .annotate(total=Sum(F("toy__price") * F("quantity")))
        .order_by("client__name")
    )
    names = [c["client__name"] for c in client_sales]
    totals = [float(c["total"] or 0) for c in client_sales]
    if not names or all(t == 0 for t in totals):
        return ""
    plt.figure(figsize=(10, max(4, len(names) // 2)))
    plt.barh(names, totals, color='skyblue')
    plt.xlabel("Сумма продаж (₽)")
    plt.ylabel("Клиенты")
    plt.title("Сумма продаж по клиентам")
    plt.tight_layout()
    return get_base64_plot()

def get_deal_amount_stats():
    amounts = list(
        Order.objects.annotate(amount=F("toy__price") * F("quantity")).values_list("amount", flat=True)
    )
    try:
        return {
            "mean": round(mean(amounts), 2) if amounts else 0,
            "median": round(median(amounts), 2) if amounts else 0,
            "mode": round(mode(amounts), 2) if amounts else "недостаточно данных",
        }
    except StatisticsError:
        return {"mean": 0, "median": 0, "mode": "недостаточно данных"}

def get_client_age_stats():
    ages = []
    for o in Order.objects.select_related("client__user"):
        if hasattr(o.client.user, "age"):
            age_val = o.client.user.age
            if age_val and age_val > 0:
                ages.append(age_val)
    return {
        "mean": round(mean(ages), 2) if ages else 0,
        "median": round(median(ages), 2) if ages else 0,
    }

def get_most_popular_type():
    toy_type = (
        ToyType.objects
        .annotate(total=Sum("toys__orders__quantity"))
        .order_by("-total")
        .first()
    )
    return toy_type.name if toy_type and toy_type.total else "Нет данных"

def get_most_profitable_type():
    toy_type = (
        ToyType.objects
        .annotate(
            profit=Sum(F("toys__orders__quantity") * F("toys__price"))
        )
        .order_by("-profit")
        .first()
    )
    return toy_type.name if toy_type and toy_type.profit else "Нет данных"

def get_statistics_context():
    return {
        "client_plot": get_client_sales_chart(),
        "stats": get_deal_amount_stats(),
        "age_stats": get_client_age_stats(),
        "most_popular_type": get_most_popular_type(),
        "most_profitable_type": get_most_profitable_type(),
    }

from django.db.models import Sum, F, Count, Q
from statistics import mean, median, mode, StatisticsError
from production.models import Order, ToyType, Toy, Client
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
from django.utils.timezone import now
from datetime import datetime

# ... (остальные функции, как у вас)

def get_price_list_by_type():
    # Средняя цена по виду игрушки
    return ToyType.objects.annotate(avg_price=Sum("toys__price")/Count("toys__id")).values("name", "avg_price")

def get_clients_by_city():
    # Группировка клиентов по городам
    return (
        Client.objects
        .values("city")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

def get_clients_detailed_by_city():
    # Список клиентов по городам
    city_clients = {}
    for client in Client.objects.all():
        city_clients.setdefault(client.city or 'Без города', []).append(client.name)
    return city_clients

def get_most_popular_toy():
    toy = (
        Toy.objects
        .annotate(sales=Sum("orders__quantity"))
        .order_by("-sales")
        .first()
    )
    return toy.name if toy and toy.sales else "Нет данных"

def get_least_popular_toy():
    toy = (
        Toy.objects
        .annotate(sales=Sum("orders__quantity"))
        .order_by("sales")
        .first()
    )
    return toy.name if toy and (toy.sales is None or toy.sales == 0) else "Нет данных"

def get_monthly_sales_by_type():
    # Ежемесячные продажи по видам
    data = {}
    for toytype in ToyType.objects.all():
        qs = (
            Order.objects
            .filter(toy__toy_type=toytype)
            .annotate(month=F('order_date__month'), year=F('order_date__year'))
            .values('year', 'month')
            .annotate(total=Sum(F('toy__price')*F('quantity')))
            .order_by('year', 'month')
        )
        data[toytype.name] = list(qs)
    return data

def get_yearly_income():
    # Доход по годам
    return (
        Order.objects
        .annotate(year=F('order_date__year'))
        .values('year')
        .annotate(income=Sum(F('toy__price')*F('quantity')))
        .order_by('year')
    )

def get_sales_trend():
    # Динамика продаж (по месяцам, для прогноза и тренда)
    qs = (
        Order.objects
        .annotate(year=F('order_date__year'), month=F('order_date__month'))
        .values('year', 'month')
        .annotate(total=Sum(F('toy__price')*F('quantity')))
        .order_by('year', 'month')
    )
    months = []
    totals = []
    for row in qs:
        label = f"{row['year']}-{row['month']:02d}"
        months.append(label)
        totals.append(float(row["total"] or 0))
    return months, totals

def get_sales_trend_plot():
    months, totals = get_sales_trend()
    if not months:
        return ""
    x = np.arange(len(months))
    plt.figure(figsize=(12, 5))
    plt.plot(x, totals, marker='o', label='Объем продаж')
    # Линейный тренд (прогноз)
    if len(x) > 1:
        z = np.polyfit(x, totals, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), "r--", label='Линейный тренд')
        plt.legend()
        plt.title("Динамика и прогноз продаж")
    plt.xticks(x, months, rotation=45)
    plt.xlabel("Месяц")
    plt.ylabel("Сумма продаж (₽)")
    plt.tight_layout()
    return get_base64_plot()

def get_statistics_context():
    return {
        "client_plot": get_client_sales_chart(),
        "stats": get_deal_amount_stats(),
        "age_stats": get_client_age_stats(),
        "most_popular_type": get_most_popular_type(),
        "most_profitable_type": get_most_profitable_type(),
        "price_list_by_type": get_price_list_by_type(),
        "clients_by_city": get_clients_by_city(),
        "clients_detailed_by_city": get_clients_detailed_by_city(),
        "most_popular_toy": get_most_popular_toy(),
        "least_popular_toy": get_least_popular_toy(),
        "monthly_sales_by_type": get_monthly_sales_by_type(),
        "yearly_income": get_yearly_income(),
        "sales_trend_plot": get_sales_trend_plot(),
    }