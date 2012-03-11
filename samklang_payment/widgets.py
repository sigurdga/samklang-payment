from samklang_menu.widgets import Widget
from samklang_payment.models import DonationCampaign
from samklang_payment.views import NETS_PRODUCTION_HOST

from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

class DonationBox(Widget):
    """Lists out total donations and how to contribute."""

    def render(self, request):
        """Function to be called to be printed"""

        campaign_slug = self.options.get("campaign")
        if campaign_slug:
            campaign = DonationCampaign.objects.get(slug=campaign_slug, payment_site=request.site)

            return render_to_string('samklang_payment/donation_box.html', {
                'amount': campaign.total_computed_donations,
                'currency': campaign.payment_site.default_currency,
                'slug': campaign_slug,
                'header': self.options.get("header"),
                'text': self.options.get("text"),

                }, context_instance=RequestContext(request))
        else:
            return ""

class DonationForm(Widget):
    """Prints out a form similar to the donation form"""

    def render(self, request):
        """Function that renders the form"""

        campaign_slug = self.options.get("campaign")
        if campaign_slug:

            from samklang_payment.models import DonationCampaign
            campaign = DonationCampaign.objects.get(slug=campaign_slug, payment_site=request.site.paymentsite)
            if campaign:
                suggestions = "-".join([str(s.amount) for s in campaign.donationsuggestion_set.all()])
                default_amount = campaign.default_amount
            else:
                suggestions = ""
                default_amount = ""

            from django.middleware.csrf import _get_new_csrf_key
            from samklang_payment.forms import DonationForm
            form = DonationForm(initial={'amount': default_amount, 'suggestions': suggestions})

            if not request.COOKIES:
                return _('<div class="error-message">You or your browser blocks our cookies. We need to use cookies to prevent cross site scripting attacks. The form will appear when cookies are allowed for this domain (%(site_domain)s). You will also need to allow cookies for the payment site (%(payment_site_domain)s).</div>') % {'site_domain': request.site.domain, 'payment_site_domain': NETS_PRODUCTION_HOST}

            if not request.COOKIES.get('csrftoken', None):
                request.META["CSRF_COOKIE"] = _get_new_csrf_key()

            return render_to_string('samklang_payment/donation_form_only.html', {
                'form': form,
                'form_action': reverse('payment-donation-create', args=[campaign_slug]),
                }, context_instance=RequestContext(request))
        else:
            return ""


class Progress(Widget):
    """Show a progress bar of how we are doing against the target"""

    def render(self, request):
        """Function that is really called"""

        campaign_slug = self.options.get("campaign")
        if campaign_slug:
            campaign = DonationCampaign.objects.get(slug=campaign_slug, payment_site=request.site)

            return render_to_string('samklang_payment/campaign_progress.html', {
            'progress': campaign.progress,
            })
        else:
            return ""

class Status(Widget):
    """Show a progress bar of how we are doing against the target"""

    def render(self, request):
        """Function that is really called"""

        campaign_slug = self.options.get("campaign")
        if campaign_slug:
            campaign = DonationCampaign.objects.get(slug=campaign_slug, payment_site=request.site)

            return render_to_string('samklang_payment/campaign_status.html', {
            'campaign': campaign,
            })
        else:
            return ""

