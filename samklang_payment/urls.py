from django.conf.urls.defaults import *
from samklang_payment.views import *

urlpatterns = patterns('',
        url(r'^campaign/$', DonationCampaignListView.as_view(), name='payment-campaign-list'),
        url(r'^campaign/(?P<slug>[-\w]+)/$', DonationCampaignDetailView.as_view(), name='payment-campaign-detail'),
        url(r'^campaign/(?P<slug>[-\w]+)/edit/$', DonationCampaignUpdateView.as_view(), name='payment-campaign-update'),
        url(r'^campaign/(?P<slug>[-\w]+)/donate/$', DonationCreateView.as_view(), name='payment-donation-create'),
        url(r'^campaign/(?P<campaign_slug>[-\w]+)/donated/(?P<slug>[-\w]+)/$', DonationDetailView.as_view(), name='payment-donation-detail'),
        url(r'^update/$', PaymentSiteUpdateView.as_view(), name='payment-site-update'),
        url(r'^configuration/$', PaymentSiteDetailView.as_view(), name='payment-site-detail'),
        )
