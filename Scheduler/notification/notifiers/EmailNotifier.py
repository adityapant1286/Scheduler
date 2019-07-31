import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from notification.notifiers.Notifier import Notifier
from utils.Utils import cfg
import configs.ConfigConstant as Cc
import utils.Constants as Sc


class EmailNotifier(Notifier):
    """
    A subclass to provide implementation to send an email notification.
    This class implements Notifier behaviour.

    """

    def __init__(self, attachments=None):
        """
        The details required to send an email are retrieved from configurations. Optionally caller can provide
        attachments for the email notification

        1. SMTP host
        2. SMTP port
        3. From email address
        4. A list of recipient emails addresses
        5. Email subject
        6. Email body

        Parameters
        ----------
        attachments : object
                     a list of file paths to be attached to a message, default None

        """
        email_stuff = cfg(Cc.NOTIFICATIONS)[0]

        self._host = email_stuff.get(Cc.SMTP_HOST)
        self._port = email_stuff.get(Cc.SMTP_PORT)
        self._from_email = email_stuff.get(Cc.FROM_EMAIL)
        self._subject = email_stuff.get(Cc.EMAIL_SUBJECT)
        self._body = email_stuff.get(Cc.EMAIL_BODY)
        self._recipients = email_stuff.get(Cc.RECIPIENT_EMAIL)
        self._attachments = attachments

    def notify(self):
        """
        Connects to SMTP server and sends an email to recipients mentioned in configurations

        """
        multipart_msg = self._build_message()
        smtp = None
        try:
            smtp = smtplib.SMTP(
                    host=self._host,
                    port=int(self._port)
            )
            smtp.sendmail(
                from_addr=self._from_email,
                to_addrs=self._recipients,
                msg=multipart_msg.as_string()
            )
        finally:
            if smtp is not None:
                smtp.close()

    def _build_message(self) -> MIMEMultipart:
        """
        Builds an email message with subject, from email, recipients and email body,
        retrieved from configurations.
        If a collection of file path (attachment) provided, then it will be set to a message.

        Returns
        --------
        MIMEMultipart
            an instance of MIMEMultipart object

        """
        msg = MIMEMultipart()
        msg[Sc.SUBJECT] = self._subject
        msg[Sc.FROM] = self._from_email
        msg[Sc.DATE] = formatdate(localtime=True)
        msg[Sc.TO] = COMMASPACE.join(self._recipients)

        body = MIMEText(self._body, 'html')
        msg.attach(body)

        for attach in self._attachments or []:
            with open(attach, "rb") as fat:
                part = MIMEApplication(
                    fat.read(),
                    Name=os.path.basename(attach)
                )
            part[Sc.CONTENT_DISPOSITION_K] = Sc.CONTENT_DISPOSITION_V % os.path.basename(attach)
            msg.attach(part)

        return msg
