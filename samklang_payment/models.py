from django.db import models
from django.utils.translation import ugettext_lazy as _

class Donation(models.Model):
    # nets' "order id" is model id
    transaction = models.CharField(_('transaction'), max_length=32, blank=True, db_index=True, help_text=_('transaction reference from nets'))
    amount = models.DecimalField(_('amount'), max_digits=7, decimal_places=2)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    captured = models.DateTimeField(_('captured'), blank=True, null=True, db_index=True)
    name = models.CharField(_('name'), max_length=80, blank=True, help_text=_('Optional. Put your name here if you want this to be linked to your name later.'))
    email = models.EmailField(_('email'), max_length=75, blank=True, help_text=_('Optional. In the future, we would like to send announcements to our contributors.'))

    def __unicode__(self):
        return u"%s %s" % (self.created.strftime("%Y-%m-%d %H:%M:%S"), self.amount)

    class Meta:
        db_table = "samklang_donation"
        verbose_name, verbose_name_plural = _('donation'), _('donations')
