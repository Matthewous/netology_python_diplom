from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
    
class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Менеджер',
                                blank=True, null=True,
                                on_delete=models.SET_NULL)
    state = models.BooleanField(verbose_name='статус получения заказов', default=True)

    # filename

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=256,verbose_name='Название')
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories', blank=True)

    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256,verbose_name='Продукт')
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', blank=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Список продуктов"
        ordering = ('-name',)


    def __str__(self):
        return self.name
    
class ProductInfo(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД')
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='product_infos', blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='product_infos', blank=True,
                             on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = "Информационный список о продуктах"
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop', 'external_id'], name='unique_product_info'),
        ]
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('editing', 'Редактирование'), ('confirmed', 'Оформлен')], default='editing')
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=100)
    delivery_date = models.DateField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def add_product(self, product_info, quantity):
        try:
            order_item = OrderItem.objects.get(order=self, product_name=product_info.product, price=product_info.price, shop=product_info.shop)
            order_item.quantity += int(quantity)
            order_item.save()
        except ObjectDoesNotExist:
            OrderItem.objects.create(
                order=self,
                product_name=product_info.product,
                quantity=quantity,
                price=product_info.price,
                shop=product_info.shop
            )
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.CharField(max_length=100)