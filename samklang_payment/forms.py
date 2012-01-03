import floppyforms as forms

from samklang_utils.forms import MarkdownTextarea
from samklang_payment.models import Donation, DonationCampaign, PaymentSite, DonationSuggestion

class DonationAmountInput(forms.TextInput):
    template_name = 'samklang_payment/donation_amount.html'

    class Media:
        js = ('js/donation_amount.js',)
        css = {
                'all': ('css/donation_amount.css',)
                }

class HiddenDonationSuggestions(forms.HiddenInput):
    template_name = 'samklang_payment/hidden_donation_suggestions.html'

    class Media:
        js = ('js/hidden_donation_suggestions.js',)

class DonationForm(forms.ModelForm):

    suggestions = forms.CharField(required=False, widget=HiddenDonationSuggestions())

    class Meta:
        model = Donation
        fields = ('suggestions', 'amount', 'name', 'email')
        widgets = {'amount': DonationAmountInput()}

class PaymentSiteUpdateForm(forms.ModelForm):

    class Meta:
        model = PaymentSite
        fields = ('merchant_id', 'test_key', 'production_key')

class DonationCampaignForm(forms.ModelForm):

    class Meta:
        model = DonationCampaign
        fields = ('name', 'description', 'test_mode', 'started', 'target_amount', 'total_donations', 'other_donations', 'default_amount', 'thank_you_text')
        widgets = {'thank_you_text': MarkdownTextarea()}

class DonationSuggestionForm(forms.ModelForm):

    class Meta:
        model = DonationSuggestion
        fields = ('amount',)
