from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


# Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    dealer_id = models.IntegerField(default=0)  # external dealer reference
    name = models.CharField(max_length=100, null=False)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),
        ('COUPE', 'Coupe'),
    ]
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SUV')

    year = models.IntegerField(
        default=datetime.date.today().year,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(datetime.date.today().year)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
