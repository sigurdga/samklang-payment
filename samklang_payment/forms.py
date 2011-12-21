import floppyforms as forms

from samklang_utils.forms import MarkdownTextarea
from samklang_payment.models import Donation, DonationCampaign, PaymentSite

class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = ('amount', 'name', 'email')

class PaymentSiteUpdateForm(forms.ModelForm):

    class Meta:
        model = PaymentSite
        fields = ('merchant_id', 'test_key', 'production_key')

class DonationCampaignForm(forms.ModelForm):

    class Meta:
        model = DonationCampaign
        fields = ('name', 'description', 'test_mode', 'started', 'target_amount', 'total_donations', 'other_donations', 'thank_you_text')
        widgets = {'thank_you_text': MarkdownTextarea()}
