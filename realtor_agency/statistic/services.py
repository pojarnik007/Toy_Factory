# services.py

from django.db.models import Sum, Count
from statistics import mean, median, mode, StatisticsError
from real_estate.models import *
from users.models import User
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def get_base64_plot():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.clf()
    return base64.b64encode(image_png).decode('utf-8')


def get_client_sales_chart():
    client_sales = (
        Sale.objects
        .select_related("client")
        .values("client__username")
        .annotate(total=Sum("real_estate_object__price"))
        .order_by("client__username")
    )

    names = [c["client__username"] for c in client_sales]
    totals = [float(c["total"]) for c in client_sales]

    plt.figure(figsize=(10, 5))
    plt.barh(names, totals, color='skyblue')
    plt.xlabel("Сумма продаж")
    plt.ylabel("Клиенты")
    plt.title("Сумма продаж по клиентам")
    plt.tight_layout()

    return get_base64_plot()


def get_deal_amount_stats():
    amounts = list(Sale.objects.values_list("real_estate_object__price", flat=True))
    try:
        return {
            "mean": round(mean(amounts), 2),
            "median": round(median(amounts), 2),
            "mode": round(mode(amounts), 2),
        }
    except StatisticsError:
        return {"mean": 0, "median": 0, "mode": "недостаточно данных"}


def get_client_age_stats():
    ages = [s.client.age for s in Sale.objects.select_related("client") if s.client.age > 0]
    return {
        "mean": round(mean(ages), 2) if ages else 0,
        "median": round(median(ages), 2) if ages else 0,
    }


def get_most_popular_category():
    category = (
        ObjectCategory.objects
        .annotate(total=Count("realestateobject"))
        .order_by("-total")
        .first()
    )
    return category.name if category else "Нет данных"


def get_most_profitable_category():
    category = (
        ObjectCategory.objects
        .annotate(profit=Sum("realestateobject__price"))
        .order_by("-profit")
        .first()
    )
    return category.name if category else "Нет данных"


def get_statistics_context():
    return {
        "client_plot": get_client_sales_chart(),
        "stats": get_deal_amount_stats(),
        "age_stats": get_client_age_stats(),
        "most_popular_type": get_most_popular_category(),
        "most_profitable_type": get_most_profitable_category(),
    }
