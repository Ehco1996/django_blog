from django.db import models

# Create your models here.


class MoneyRecord(models.Model):
    '''充值流水单号记录'''

    info_code = models.CharField(
        '流水号',
        max_length=64,
        unique=True,
    )

    time = models.DateTimeField(
        '时间',
        auto_now_add=True
    )

    amount = models.DecimalField(
        '金额',
        decimal_places=2,
        max_digits=10,
        default=0,
        null=True,
        blank=True,
    )

    money_code = models.CharField(
        '充值码',
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.info_code

    class Meta:
        verbose_name_plural = '交易记录'
        ordering = ('-time',)
