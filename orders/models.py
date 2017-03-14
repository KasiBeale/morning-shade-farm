from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def multiple_of_ten(value):
    if value % 10 != 0:
        raise ValidationError('{} is not a multiple of 10.'.format(value))


def greater_than_zero(value):
    if value <= 0:
        raise ValidationError('{} is not greater than 0.'.format(value))


def after_now(value):
    if value < timezone.now():
        raise ValidationError("The date & time cannot be in the past.")

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('FULFILLED', 'Fulfilled'),
        ('CANCELED', 'Canceled'),
    )
    pickup_date = models.DateTimeField(validators=[after_now,])
    quantity = models.IntegerField(validators=[multiple_of_ten, greater_than_zero])
    requester_name = models.CharField(max_length=128)
    requester_email = models.CharField(max_length=128)
    requester_phone_number = PhoneNumberField(blank=True)
    comments = models.TextField(blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=128, default="PENDING")
    total_cost = models.DecimalField(max_digits=16, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.get_cost_per_pound()
        return super(Order, self).save(*args, **kwargs)

    def get_cost_per_pound(self):
        """
        :return: a Decimal of the cost per pound of berries that this order qualifies for,
        based on its quantity.
        """
        # Get the first (lowest) price object which this # of pounds qualifies for. The first
        # object will be the highest minimum (and presumably the lowest price) because the Price
        # objects are ordered descending by min quantity
        price = Price.objects.filter(min_quantity__lte=self.quantity).first()
        return price.cost_per_pound

    def __str__(self):
        return "{} order for {} pounds on {} for {}".format(
            self.status.capitalize(), self.quantity, self.pickup_date, self.requester_name)
    description = property(__str__)


class Price(models.Model):
    """
    """
    # eventually can add a FK to which product this is for
    cost_per_pound = models.DecimalField(max_digits=8, decimal_places=2)
    min_quantity = models.IntegerField()

    class Meta:
        ordering = ["-min_quantity"]

    def __str__(self):
        return "{} per lb. for orders over {} lbs.".format(self.cost_per_pound, self.min_quantity)
