from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext as _


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Group(models.Model):
    title = models.CharField(verbose_name=_('Name'), max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class Item(models.Model):
    def validate_stock(value):
        if value < 0:
            raise ValidationError(
                ('stock is not enough!')
            )

    title = models.CharField(verbose_name=_('Name'), max_length=200)
    group = models.ForeignKey(Group, verbose_name=_('Group'))
    price = models.PositiveIntegerField(verbose_name=_('Price'), default=0, validators=[validate_stock])
    comment = models.TextField(verbose_name=_('Comment'), max_length=500)
    image = models.ImageField(verbose_name=_('Image'), upload_to="media/images", default="media/images/avatar.jpg")
    stock = models.PositiveIntegerField(verbose_name=_('Stock'), default=0)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS = (
        ('requested', _('Requested')),
        ('canceled', _('Canceled')),
        ('pending', _('Pending')),
        ('finished', _('Finished')),
    )
    items = models.ManyToManyField(Item, verbose_name=_('Product'))
    time = models.DateTimeField(verbose_name=_('Time'), auto_now_add=True)
    total_price = models.PositiveIntegerField(verbose_name=_('Total_price'), default=0)
    status = models.CharField(verbose_name=_('Status'), max_length=9, choices=STATUS, default='requested')
    owner = models.ForeignKey('auth.User', related_name='orders', verbose_name=_('Owner'), on_delete=models.CASCADE,
                              default=-1)
    __original_status = 'requested'

    def __init__(self, *args, **kwargs):  # initialy saves last order's status to order's original status
        super(Order, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, force_insert=False, force_update=False, *args,
             **kwargs):  # checks if order's status was changed and canceled ,increase item's stock
        if self.status != self.__original_status and self.status == 'canceled':
            for item in self.items.all():
                item.stock += 1
                item.save()

        super(Order, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
