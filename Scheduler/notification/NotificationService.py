from notification.notifiers.Notifier import Notifier
import utils.Constants as Sc
from utils.Utils import current_time_in_millis, time_taken
from auditlogging.Auditor import audit_params


def notify(notifier: Notifier):
    """
    This module allows to send a notification based on the custom implementation of the
    ``Notifier`` abstract class. A developer needs to provide implementation for the notifier.

    The notifier dependency will be injected by the caller as per the use case. This behaviour
    allows to plug in either existing notifier or custom notifiers.

    This method also captures general audit log.

    Parameters
    ----------
    notifier : Notifier
                an instance of custom implementation of ``Notifier``

    """
    _start = current_time_in_millis()
    audit_params(Sc.OPERATION_NOTIFICATION,
                 Sc.STATUS_PROCESSING,
                 'Sending notification')

    notifier.notify()

    audit_params(Sc.OPERATION_NOTIFICATION,
                 Sc.STATUS_COMPLETE,
                 'Notification sent' + time_taken(_start))
