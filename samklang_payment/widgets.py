from django.utils.translation import ugettext as _
from samklang_menu.widgets import Widget
from samklang_payment.models import Donation, DonationCampaign
from django.db.models import Sum
from django.template.loader import render_to_string
from django.template.context import RequestContext

class DonationBox(Widget):
    """Lists out total donations and how to contribute."""

    def render(self, request):
        """Function to be called to be printed"""

        campaign_id = self.options.get("campaign")
        if campaign_id:
            campaign = DonationCampaign.objects.get(pk=campaign_id, payment_site=request.site)

            return render_to_string('samklang_payment/donation_box.html', {
                'amount': campaign.total_computed_donations,
                'currency': campaign.payment_site.default_currency,
                'slug': campaign.slug,
                'header': self.options.get("header"),
                'text': self.options.get("text"),

                }, context_instance=RequestContext(request))
        else:
            return ""

class Progress(Widget):
    """Show a progress bar of how we are doing against the target"""

    def render(self, request):
        """Function that is really called"""

        campaign_id = self.options.get("campaign")
        if campaign_id:
            campaign = DonationCampaign.objects.get(pk=campaign_id, payment_site=request.site)

            return render_to_string('samklang_payment/campaign_progress.html', {
            'progress': campaign.progress,
            })
        else:
            return ""
