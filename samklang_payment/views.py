from urllib2 import urlopen
from urllib import quote
from BeautifulSoup import BeautifulSoup
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from samklang_payment.models import Donation
from samklang_payment.forms import DonationForm
from pyrfc3339 import parse
from django.utils.translation import ugettext as _

NETS_TEST_HOST = "epayment-test.bbs.no"
NETS_PRODUCTION_HOST = "epayment.bbs.no"

class CreateDonationView(CreateView):
    model = Donation
    form_class = DonationForm

    def form_valid(self, form):
        """We get back form data, save the object, and initiates payment at Nets"""

        # save here to get id
        donation = form.save()
        redirect_url = "http://"+self.request.get_host()+reverse('payment-donate')
        if settings.NETS_TEST_MODE:
            nets_host = NETS_TEST_HOST
        else:
            nets_host = NETS_PRODUCTION_HOST
        url = "https://%(nets_host)s/Netaxept/Register.aspx?merchantId=%(merchant_id)d&token=%(token)s&orderNumber=%(order_number)d&amount=%(amount)d&currencyCode=NOK&redirecturl=%(redirect_url)s" % {
                'nets_host': nets_host,
                'amount': int(donation.amount*100),
                'merchant_id': settings.NETS_MERCHANT_ID,
                'order_number': donation.id,
                'token': quote(settings.NETS_TOKEN),
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
        url = "https://%(nets_host)s/Terminal/default.aspx?merchantid=%(merchant_id)d&transactionid=%(transaction_id)s" % {
                'nets_host': nets_host,
                'transaction_id': transaction_id,
                'merchant_id': settings.NETS_MERCHANT_ID,
                }
        return HttpResponseRedirect(url)


    def get(self, request, *args, **kwargs):
        if settings.NETS_TEST_MODE:
            nets_host = NETS_TEST_HOST
        else:
            nets_host = NETS_PRODUCTION_HOST
        if settings.NETS_TOKEN == 0:
            return render_to_response('samklang_payment/error.html',
                        {'error': _('Payment site authentication is not yet set up.')},
                        context_instance=RequestContext(request))

        if 'transactionId' in request.GET:
            # Last step: run transaction and get status from nets
            transaction_id = request.GET.get('transactionId', None)
            if not transaction_id:
                return render_to_response('samklang_payment/error.html',
                        {'error': _('Transaction ID was empty')},
                        context_instance=RequestContext(request))

            url = "https://%(nets_host)s/Netaxept/Process.aspx?merchantId=%(merchant_id)d&token=%(token)s&transactionId=%(transaction_id)s&operation=SALE" % {
                    'nets_host': nets_host,
                    'transaction_id': transaction_id,
                    'merchant_id': settings.NETS_MERCHANT_ID,
                    'token': quote(settings.NETS_TOKEN),
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
                return HttpResponseRedirect("/")
            else:
                return render_to_response('samklang_payment/error.html',
                        {'error': "%s: %s" % (response_code, handle_error(data))},
                        context_instance=RequestContext(request))
        else:
            return super(CreateDonationView, self).get(request, *args, **kwargs)


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