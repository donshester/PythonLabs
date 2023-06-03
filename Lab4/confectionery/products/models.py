from django.db import models

UNIT_CHOICES = (
    ('pcs', 'Pieces'),
    ('l', 'Liters'),
    ('g', 'Grams'),
    ('kg', 'Kilograms'),
    ('ml', 'Milliliters'),
    ('boxes', 'Boxes'),
    ('packets', 'Packets'),
    ('jars', 'Jars'),
    ('slices', 'Slices'),
    ('servings', 'Servings'),
    ('m', 'Meters'),
    ('cm', 'Centimeters')
)


class Manufacturer(models.Model):
    name = models.CharField(max_length=200,
                            help_text='Enter manufacturer name')

    country = models.CharField(max_length=20)
    foundation_date = models.DateField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200,
                            help_text='Enter category name')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def is_available(self):
        return self.quantity > 0

    class Meta:
        permissions = [
            ('view_quantity', 'Can view quantity'),
        ]

    def __str__(self):
        return self.name
