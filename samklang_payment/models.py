from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.db.models import Sum
from samklang_utils import markdown
#from stdimage import StdImageField

class PaymentSite(models.Model):
    site = models.OneToOneField(Site, verbose_name=_('site'))
    default_currency = models.CharField(_('default currency'), max_length=3, default="NOK")
    merchant_id = models.CharField(_('merchant id'), max_length=32, blank=True)
    test_key = models.CharField(_('test key'), max_length=32, blank=True)
    production_key = models.CharField(_('production key'), max_length=32, blank=True)

    def __unicode__(self):
        return self.site.name

    @models.permalink
    def get_absolute_url(self):
        return ('payment-site-detail',)

    class Meta:
        verbose_name, verbose_name_plural = _('site'), _('sites')


class DonationCampaign(models.Model):
    payment_site = models.ForeignKey(PaymentSite, verbose_name=_('payment site'))
    name = models.CharField(_('name'), max_length=80)
    slug = models.SlugField(_('slug'))
    description = models.CharField(_('description'), max_length=250, blank=True)
    test_mode = models.BooleanField(_('test mode'), default=True, help_text=_("Run this campaign in test mode, not transfering real money."))
    target_amount = models.DecimalField(_('target amount'), max_digits=9, decimal_places=2, blank=True, null=True)
    total_donations = models.DecimalField(_('total donations'), max_digits=9, decimal_places=2, help_text=_('The total amount of donations to this campaign. Fill in this value OR "other donations".'), blank=True, null=True)
    other_donations = models.DecimalField(_('other donations'), max_digits=9, decimal_places=2, help_text=_('Donations made elsewhere to the system. If this is used, the total will be updated automatically.'), blank=True, null=True)
    default_amount = models.DecimalField(_('default amount'), max_digits=9, decimal_places=2, blank=True, null=True)
    # next line or special page with info about the transaction?
    #thank_you_page_url = models.CharField(_('thank you page url'), max_length=100, help_text=_("Redirect to this page to thank the users for their contributions"))
    thank_you_text = models.TextField(_('thank you text'), blank=True)
    thank_you_text_html = models.TextField(null=True, blank=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    started = models.DateTimeField(_('started'), help_text=('Official start date'))
    updated = models.DateTimeField(_('updated'), auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('payment-campaign-detail', [self.slug])

    class Meta:
        verbose_name, verbose_name_plural = _('campaign'), _('campaigns')

    def save(self, *args, **kwargs):
        self.thank_you_text_html = markdown(self.thank_you_text.strip())
        super(DonationCampaign, self).save(*args, **kwargs)

    @property
    def online_donations(self):
        return self.donation_set.filter(captured__isnull=False).aggregate(Sum('amount'))['amount__sum']

    @property
    def total_computed_donations(self):
        if self.other_donations:
            return self.other_donations + self.online_donations
        else:
            return self.total_donations

    @property
    def other_computed_donations(self):
        if self.other_donations:
            return self.other_donations
        else:
            return self.total_donations - self.online_donations

    @property
    def progress(self):
        return "%.1f" % (self.total_computed_donations *100 / self.target_amount)


class DonationSuggestion(models.Model):
    """Suggestions for donations, will appear with the forms using DonationAmountInput"""

    campaign = models.ForeignKey(DonationCampaign, verbose_name=_('campaign'))
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('amount'))

    class Meta:
        ordering = ('amount',)

    def __unicode__(self):
        return "%.2f" % self.amount

    @models.permalink
    def get_absolute_url(self):
        return ('view_or_url_name' )


class DonationManager(models.Manager):

    #def get_query_set(self):
    #    return super(CapturedManager, self).get_query_set().filter(captured__isnull=False)

    def captured(self):
        return self.get_query_set().filter(captured__isnull=False)

class Donation(models.Model):
    # nets' "order id" is model id
    campaign = models.ForeignKey(DonationCampaign, verbose_name=('campaign'), null=True, blank=True)
    transaction = models.CharField(_('transaction'), max_length=32, blank=True, db_index=True, help_text=_('transaction reference from nets'))
    amount = models.DecimalField(_('amount'), max_digits=7, decimal_places=2)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    captured = models.DateTimeField(_('captured'), blank=True, null=True, db_index=True)
    name = models.CharField(_('name'), max_length=80, blank=True, help_text=_('Optional. Put your name here if you want this to be linked to your name later.'))
    email = models.EmailField(_('email'), max_length=75, blank=True, help_text=_('Optional. In the future, we would like to send announcements to our contributors.'))

    # managers
    objects = DonationManager()
    #captured_transactions = CapturedManager()

    def __unicode__(self):
        return u"%s %s" % (self.created.strftime("%Y-%m-%d %H:%M:%S"), self.amount)

    class Meta:
        ordering = ("-created",)
        verbose_name, verbose_name_plural = _('donation'), _('donations')
