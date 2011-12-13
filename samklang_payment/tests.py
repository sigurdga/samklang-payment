from django.test import TestCase
from datetime import datetime
from pytz import utc
from samklang_payment.views import get_transaction_id, get_execution_time

class TestDonation(TestCase):


    def test_get_transaction_id(self):
        """
        From register response, get the transaction id
        """

        example_response = """<?xml version="1.0"?>
<RegisterResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <TransactionId>6d16d881b9d1497a8b9bae21eaf7e760</TransactionId>
</RegisterResponse>"""

        transaction_id = get_transaction_id(example_response)
        self.assertEqual(u"6d16d881b9d1497a8b9bae21eaf7e760", transaction_id)

    def test_get_execution_time(self):

        example_response = """<?xml version="1.0" ?>
<ProcessResponse xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <Operation>AUTH</Operation>
    <ResponseCode>OK</ResponseCode>
   <AuthorizationId>064392</AuthorizationId>
   <TransactionId>b127f98b77f741fca6bb49981ee6e846</TransactionId>
   <ExecutionTime>2009-12-16T11:17:54.633125+01:00</ExecutionTime>
   <MerchantId>9999997</MerchantId>
</ProcessResponse>"""

        correct_datetime = datetime(2009, 12, 16, 10, 17, 54, 633125, utc)
        execution_time = get_execution_time(example_response)
        self.assertEqual(correct_datetime, execution_time)
