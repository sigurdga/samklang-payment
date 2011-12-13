from django.db import models
from django.utils.translation import ugettext_lazy as _

class Donation(models.Model):
    # nets' "order id" is model id
    transaction = models.CharField(max_length=32, blank=True, db_index=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    captured = models.DateTimeField(blank=True, null=True, db_index=True)
    name = models.CharField(max_length=80, blank=True, help_text=_('Optional'))
    email = models.EmailField(max_length=75, blank=True, help_text=_('Optional'))

    def __unicode__(self):
        return u"%s %s" % (self.created.strftime("%Y-%m-%d %H:%M:%S"), self.amount)

    class Meta:
        db_table = "samklang_donation"
        verbose_name, verbose_name_plural = _('donation'), _('donations')
