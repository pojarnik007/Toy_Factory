# Generated by Django 5.2.1 on 2025-06-02 09:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PickupPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('active', models.BooleanField(default=True, verbose_name='Активна')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Код')),
                ('discount_percent', models.PositiveIntegerField(default=0, verbose_name='Скидка %')),
                ('active', models.BooleanField(default=True, verbose_name='Активен')),
                ('expires_at', models.DateField(blank=True, null=True, verbose_name='Действует до')),
            ],
        ),
        migrations.RemoveField(
            model_name='toy',
            name='toy_model',
        ),
        migrations.RemoveField(
            model_name='client',
            name='address',
        ),
        migrations.RemoveField(
            model_name='client',
            name='code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_date',
        ),
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='client',
            name='is_wholesale',
            field=models.BooleanField(default=False, verbose_name='Оптовый клиент'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Создан'), ('processing', 'В обработке'), ('completed', 'Завершён'), ('cancelled', 'Отменён')], default='created', max_length=20, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='toy',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='toy',
            name='in_stock',
            field=models.PositiveIntegerField(default=0, verbose_name='В наличии'),
        ),
        migrations.AddField(
            model_name='toytype',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(blank=True, max_length=100, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Имя/Компания'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='production.client'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='order',
            name='toy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='production.toy'),
        ),
        migrations.AlterField(
            model_name='toy',
            name='code',
            field=models.CharField(max_length=30, unique=True, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='toy',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='toy',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='В продаже'),
        ),
        migrations.AlterField(
            model_name='toy',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='toy',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='toy',
            name='toy_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toys', to='production.toytype'),
        ),
        migrations.AlterField(
            model_name='toytype',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='toytype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название типа'),
        ),
        migrations.AddField(
            model_name='order',
            name='pickup_point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='production.pickuppoint'),
        ),
        migrations.CreateModel(
            name='SaleAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('total_orders', models.PositiveIntegerField(verbose_name='Всего заказов')),
                ('total_income', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Сумма продаж')),
                ('most_popular_toy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='production.toy')),
            ],
        ),
        migrations.DeleteModel(
            name='ToyModel',
        ),
    ]
