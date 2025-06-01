from django.db import models

class ToyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ToyModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Toy(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    toy_type = models.ForeignKey(ToyType, on_delete=models.CASCADE)
    toy_model = models.ForeignKey(ToyModel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Client(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.city})"

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE)
    order_date = models.DateField()
    delivery_date = models.DateField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.pk} - {self.client.name}"
