import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    use_as_menu = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_products(self):
        return self.products.all()


class Product(models.Model): # polo tshirt
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('publish', 'Publish'),
        ('unpublish', 'Unpublish'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    specifications = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name


class ProductImage(models.Model):  
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductVariant(models.Model):  #   color: red, blue, green | size: small, large, exlarge
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(max_length=255)
    attributes = models.JSONField(blank=True, null=True)  # Example: {"material": "cotton", "pattern": "striped"}
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = uuid.uuid4().hex[:10].upper()

        super().save(*args, **kwargs)


class ProductStock(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.DO_NOTHING, related_name='variants')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self, *args, **kwargs):
        return f"{self.product_variant.sku}"
