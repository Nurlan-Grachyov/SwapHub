from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ExchangeOffer(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Ожидает')),
        ('accepted', _('Принято')),
        ('declined', _('Отклонено'))
    )

    ad_sender = models.ForeignKey(
        to='Product',  # Предположительно у вас есть модель Advertisement
        related_name='offered_ads',
        on_delete=models.CASCADE,
        verbose_name=_("Объявление отправителя")
    )

    ad_receiver = models.ForeignKey(
        to='Product',
        related_name='received_offers',
        on_delete=models.CASCADE,
        verbose_name=_("Объявление получателя")
    )

    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_exchange_offers',
        on_delete=models.CASCADE,
        verbose_name=_("Отправитель")
    )

    receiver_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_exchange_offers',
        on_delete=models.CASCADE,
        verbose_name=_("Получатель")
    )

    comment = models.TextField(blank=True, verbose_name=_("Комментарий"))

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Статус предложения")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Предложение обмена")
        verbose_name_plural = _("Предложения обмена")

    def __str__(self):
        return f'{self.ad_sender} -> {self.ad_receiver}'
