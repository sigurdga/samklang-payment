from django.contrib import admin
from samklang_payment.models import Donation, DonationCampaign, PaymentSite, DonationSuggestion

# will work when 1.4 is out
#class CapturedStatusfilter(SimpleListFilter):

    #title = _('Transaction status')
    #parameter_name = 'captured'

    #def lookups(self, request, model_admin):
        #return (
                #(True, _('Verified transactions')),
                #(False, _('Failed transactions')),
                #)

    #def queryset(self, request, queryset):
        #if self.value == True:
            #queryset.exclude(captured__isnull=True)
        #else:
            #queryset.exclude(captured__isnull=False)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'created', 'captured', 'amount')
    list_filter = ('campaign', 'captured',)
    #list_filter = (CapturedStatusfilter,)


admin.site.register(Donation, DonationAdmin)
admin.site.register(PaymentSite)
admin.site.register(DonationCampaign)
admin.site.register(DonationSuggestion)
