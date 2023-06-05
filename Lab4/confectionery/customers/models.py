from datetime import date
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        Group,
        related_name='customer_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customer_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def get_age(self):
        current_date = date.today()
        age = current_date.year - self.date_of_birth.year
        if (
            current_date.month < self.date_of_birth.month
            or (current_date.month == self.date_of_birth.month and current_date.day < self.date_of_birth.day)
        ):
            age -= 1
        return age

    def __str__(self):
        return self.username


def setup_groups():
    staff_group, _ = Group.objects.get_or_create(name='Staff')
    customer_group, _ = Group.objects.get_or_create(name='Customer')
    content_type = ContentType.objects.get(app_label='products', model='product')
    permissions = Permission.objects.filter(content_type=content_type,
                                            codename__in=['change_product', 'delete_product'])
    staff_group.permissions.set(permissions)
    staff_group.save()
    customer_group.save()


