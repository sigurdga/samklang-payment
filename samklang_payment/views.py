from urllib2 import urlopen
from urllib import quote
from BeautifulSoup import BeautifulSoup
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from samklang_payment.models import Donation, PaymentSite, DonationCampaign, DonationSuggestion
from samklang_payment.forms import DonationForm, PaymentSiteUpdateForm, DonationCampaignForm, DonationSuggestionForm
from pyrfc3339 import parse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

NETS_TEST_HOST = "epayment-test.bbs.no"
NETS_PRODUCTION_HOST = "epayment.bbs.no"

class DonationDetailView(DetailView):
    model = Donation
    slug_field = 'transaction'

class DonationCreateView(CreateView):
    model = Donation
    form_class = DonationForm

    def form_valid(self, form):
        """We get back form data, save the object, and initiates payment at Nets"""

        # save here to get id
        donation = form.save(commit=False)
        donation.campaign = DonationCampaign.objects.get(slug=self.kwargs.get('slug'), payment_site=self.request.site.paymentsite)
        redirect_url = "http://"+self.request.get_host()+reverse('payment-donation-create', kwargs={'slug': donation.campaign.slug})
        configuration = donation.campaign.payment_site
        if not configuration:
            return render_to_response('samklang_payment/error.html',
                        {'error': _('Payment site authentication is not yet set up.')},
                        context_instance=RequestContext(self.request))
        donation.save()
        if donation.campaign.test_mode:
            nets_host = NETS_TEST_HOST
            token = configuration.test_key
        else:
            nets_host = NETS_PRODUCTION_HOST
            token = configuration.production_key

        url = "https://%(nets_host)s/Netaxept/Register.aspx?merchantId=%(merchant_id)s&token=%(token)s&orderNumber=%(order_number)d&amount=%(amount)d&currencyCode=%(currency_code)s&redirecturl=%(redirect_url)s" % {
                'nets_host': nets_host,
                'amount': int(donation.amount*100),
                'merchant_id': configuration.merchant_id, #settings.NETS_MERCHANT_ID,
                'order_number': donation.id,
                'token': quote(token),
                'currency_code': configuration.default_currency.upper(),
                'redirect_url': redirect_url,
                }

        response = urlopen(url)
        data = response.read()
        try:
            transaction_id = get_transaction_id(data)
        except ValueError, e:
            return render_to_response('samklang_payment/error.html',
                    {'error': e},
                    context_instance=RequestContext(self.request))

        #if no error, redirect user to online payment terminal
        donation.transaction = transaction_id
        donation.save()
        url = "https://%(nets_host)s/Terminal/default.aspx?merchantid=%(merchant_id)s&transactionid=%(transaction_id)s" % {
                'nets_host': nets_host,
                'transaction_id': transaction_id,
                'merchant_id': configuration.merchant_id,
                }
        return HttpResponseRedirect(url)


    def get(self, request, *args, **kwargs):
        campaign = DonationCampaign.objects.get(slug=self.kwargs.get('slug'), payment_site=self.request.site.paymentsite)
        configuration = campaign.payment_site
        if not configuration:
            return render_to_response('samklang_payment/error.html',
                        {'error': _('Payment site authentication is not yet set up.')},
                        context_instance=RequestContext(self.request))
        if campaign.test_mode:
            nets_host = NETS_TEST_HOST
            token = configuration.test_key
        else:
            nets_host = NETS_PRODUCTION_HOST
            token = configuration.production_key

        if 'transactionId' in request.GET:
            # Last step: run transaction and get status from nets
            transaction_id = request.GET.get('transactionId', None)
            if not transaction_id:
                return render_to_response('samklang_payment/error.html',
                        {'error': _('Transaction ID was empty')},
                        context_instance=RequestContext(request))

            url = "https://%(nets_host)s/Netaxept/Process.aspx?merchantId=%(merchant_id)s&token=%(token)s&transactionId=%(transaction_id)s&operation=SALE" % {
                    'nets_host': nets_host,
                    'transaction_id': transaction_id,
                    'merchant_id': configuration.merchant_id,
                    'token': quote(token),
                    }
            response = urlopen(url)
            data = response.read()
            try:
                response_code = get_response_code(data)
                execution_time = get_execution_time(data)
            except ValueError, e:
                return render_to_response('samklang_payment/error.html',
                        {'error': e},
                        context_instance=RequestContext(request))

            if response_code == "OK":
                donation = Donation.objects.get(transaction=transaction_id)
                donation.captured = execution_time
                donation.save()
                return HttpResponseRedirect(reverse('payment-donation-detail', kwargs={'campaign_slug': donation.campaign.slug, 'slug': transaction_id}))
            else:
                return render_to_response('samklang_payment/error.html',
                        {'error': "%s: %s" % (response_code, handle_error(data))},
                        context_instance=RequestContext(request))
        else:
            return super(DonationCreateView, self).get(request, *args, **kwargs)


def handle_error(text):
    soup = BeautifulSoup(text)
    message_tag = soup.find("message")
    if not message_tag:
        return "Unknown error"
    else:
        return message_tag.text

def get_transaction_id(text):
    soup = BeautifulSoup(text)
    transaction_id_tag = soup.find("transactionid")
    if not transaction_id_tag:
        error = handle_error(text)
        raise ValueError(error)
    else:
        return transaction_id_tag.text

def get_response_code(text):
    soup = BeautifulSoup(text)
    response_code = soup.find("responsecode")
    if not response_code:
        error = handle_error(text)
        raise ValueError(error)
    else:
        return response_code.text

def get_execution_time(text):
    soup = BeautifulSoup(text)
    execution_time = soup.find("executiontime")
    if not execution_time:
        error = handle_error(text)
        raise ValueError(error)
    else:
        return parse(execution_time.text)

class PaymentSiteDetailView(DetailView):
    model = PaymentSite

    def get_object(self):
        return self.request.site.paymentsite

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentSiteDetailView, self).dispatch(*args, **kwargs)

class PaymentSiteUpdateView(UpdateView):
    model = PaymentSite
    form_class = PaymentSiteUpdateForm

    def get_object(self):
        return self.request.site.paymentsite

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentSiteUpdateView, self).dispatch(*args, **kwargs)

class DonationCampaignListView(ListView):
    model = DonationCampaign

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DonationCampaignListView, self).dispatch(*args, **kwargs)

class DonationCampaignDetailView(DetailView):
    model = DonationCampaign

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DonationCampaignDetailView, self).dispatch(*args, **kwargs)

class DonationCampaignUpdateView(UpdateView):
    model = DonationCampaign
    form_class = DonationCampaignForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DonationCampaignUpdateView, self).dispatch(*args, **kwargs)

class DonationSuggestionCreateView(CreateView):
    model = DonationSuggestion
    form_class = DonationSuggestionForm

    def form_valid(self, form):
        suggestion = form.save(commit=False)
        campaign = DonationCampaign.objects.get(slug=self.kwargs['slug'])
        suggestion.campaign = campaign
        suggestion.save()
        return HttpResponseRedirect(campaign.get_absolute_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DonationSuggestionCreateView, self).dispatch(*args, **kwargs)

class DonationSuggestionUpdateView(UpdateView):
    model = DonationSuggestion
    form_class = DonationSuggestionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DonationSuggestionUpdateView, self).dispatch(*args, **kwargs)

class DonationSuggestionDeleteView(DeleteView):
    model = DonationSuggestion

    def get_object(self):
        suggestion = DonationSuggestion.objects.get(campaign__slug=self.kwargs.get('slug'), amount=self.kwargs.get('amount'))
        return suggestion

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        campaign = self.object.campaign
        self.object.delete()
        return HttpResponseRedirect(campaign.get_absolute_url())


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DonationSuggestionDeleteView, self).dispatch(*args, **kwargs)
