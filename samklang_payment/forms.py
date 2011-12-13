import floppyforms as forms

from samklang_payment.models import Donation

class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = ('amount', 'name', 'email')

