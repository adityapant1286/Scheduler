from jobs.Job import Job
from utils.Utils import isnone


class PaymentCreditMemo(Job):
    config = {}
    def __init__(self, job_name: str, cfg):
        self._job_name = job_name

    def goal(self):
        # export payment - (Payment.Status='Processed' AND Payment.UnappliedAmount > 0)
        # AND  Account.AccountNumber != 'SUNDRYDEBTOR'
        # AND Account.TotalInvoiceBalance > 0
        # order by  Payment.CreatedDate desc

        # get exported file
        # loop each payment
        # each open invoice
        # check invoice parameters
        # apply payments
        # check response
        print("Hello from test job ")

    def name(self) -> str:
        return self._job_name
