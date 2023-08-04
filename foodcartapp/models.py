from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field import serializerfields
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

REGION_CODE = 'RU'


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    address = models.CharField('адрес', max_length=200)
    firstname = models.CharField('имя', max_length=50)
    lastname = models.CharField('фамилия', max_length=50)
    phonenumber = PhoneNumberField('телефон', region=REGION_CODE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.address}'


class OrderItem(models.Model):
    product = models.ForeignKey('Product',
                                related_name='items',
                                on_delete=models.CASCADE,
                                verbose_name='продукт в заказе',
                                )
    order = models.ForeignKey('Order',
                              related_name='items',
                              on_delete=models.CASCADE,
                              verbose_name='заказ',
                              )
    quantity = models.IntegerField('количество',
                                   validators=[
                                       MinValueValidator(0),
                                   ],
                                   )

    class Meta:
        verbose_name = 'наименование'
        verbose_name_plural = 'наименований'

    def __str__(self):
        return f'{self.product} {self.order}'


class OrderItemSerializer(ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderSerializer(ModelSerializer):
    phonenumber = serializerfields.PhoneNumberField()
    products = OrderItemSerializer(many=True,
                                   allow_empty=False,
                                   source='items',
                                   )

    class Meta:
        model = Order
        fields = (
            'address',
            'firstname',
            'lastname',
            'phonenumber',
            'products',
        )

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for order_item in items:
            OrderItem.objects.create(order=order, **order_item)

        return order
