from django.db import models


# Create your models here.


class Customer(models.Model):
    """Клиенты"""

    tg_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")

    name = models.CharField(max_length=255, verbose_name="Имя")

    phone = models.CharField(
        max_length=20, verbose_name="Телефон", blank=True, null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Bouquet(models.Model):
    """Модель букетов"""

    OCCASION_CHOICES = [
        ("birthday", "День рождения"),
        ("wedding", "Свадьба"),
        ("school", "В школу"),
        ("no_reason", "Без повода"),
        ("other", "Другой повод"),
    ]
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="bouquets/", verbose_name="Фото букета")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    occasion = models.CharField(
        max_length=255, choices=OCCASION_CHOICES, verbose_name="Повод"
    )
    essence_bouquet = models.TextField(default="Нет заметок",
                                       blank=True,
                                       verbose_name='Смысл букета')
    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Order(models.Model):
    """Заказы"""

    STATUS_CHOICES = [
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("delivered", "Доставлен"),
        ("canceled", "Отменен"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="Клиент"
    )
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, verbose_name="Букет")
    address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    delivery_time = models.DateTimeField(verbose_name="Дата и время доставки")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    def __str__(self):
        return f"Заказ {self.id} - {self.customer.name} - {self.status}"


class Courier(models.Model):
    """Курьеры"""

    tg_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return self.name


class Florist(models.Model):
    """Флористы"""

    tg_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return self.name


class Payment(models.Model):
    """Оплата"""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    payment_id = models.CharField(
        max_length=255, unique=True, verbose_name="ID платежа"
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "В ожидании"), ("paid", "Оплачен"), ("failed", "Ошибка")],
        verbose_name="Статус оплаты",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    def __str__(self):
        return f"Оплата {self.payment_id} - {self.status}"


class Statistics(models.Model):
    customer_name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="Заказчик"
    )
    bouquet_name = models.ForeignKey(
        Bouquet, on_delete=models.CASCADE, verbose_name="Букеты"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")


class Consultation(models.Model):
    customer_name = models.CharField(max_length=255, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата запроса")

    def __str__(self):
        return f"{self.customer_name} - {self.phone}"
