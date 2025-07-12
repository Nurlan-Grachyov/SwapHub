from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    STATUS_CHOICES = [
        ("new", _("Новый")),
        ("used", _("Бывший в употреблении")),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    description = models.TextField(verbose_name=_("Описание"))
    image_url = models.URLField(blank=True, null=True, verbose_name=_("URL изображения"))
    category = models.CharField(max_length=100, verbose_name=_("Категория"))
    condition = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name=_("Состояние"),
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата публикации"))

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    def __str__(self):
        return f"{self.title}"
