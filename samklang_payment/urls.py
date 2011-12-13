from django.conf.urls.defaults import *
from samklang_payment.views import *

urlpatterns = patterns('',
        url(r'^donation/$', CreateDonationView.as_view(), name='payment-donate'),
        )
