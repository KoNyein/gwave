from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, default='📦')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.emoji} {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    emoji = models.CharField(max_length=10, default='🛍️')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price_mmk = models.DecimalField(max_digits=12, decimal_places=0)
    stock = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.emoji} {self.name}"

    @property
    def price_thb(self):
        return round(float(self.price_mmk) / 85, 0)

    @property
    def is_low_stock(self):
        return self.stock <= self.low_stock_threshold and self.stock > 0

    @property
    def is_out_of_stock(self):
        return self.stock == 0


class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('transfer', 'Transfer'),
        ('card', 'Card'),
    ]
    CURRENCY_CHOICES = [
        ('MMK', 'Myanmar Kyat'),
        ('THB', 'Thai Baht'),
    ]

    sale_number = models.CharField(max_length=20, unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='MMK')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    subtotal = models.DecimalField(max_digits=14, decimal_places=0)
    discount = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=0)
    cash_received = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    change_amount = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    cashier = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Sale #{self.sale_number} — {self.total} {self.currency}"

    def save(self, *args, **kwargs):
        if not self.sale_number:
            last = Sale.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.sale_number = f"POS{str(num).zfill(6)}"
        super().save(*args, **kwargs)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)  # snapshot
    product_emoji = models.CharField(max_length=10, default='🛍️')
    price_mmk = models.DecimalField(max_digits=12, decimal_places=0)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=14, decimal_places=0)

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
