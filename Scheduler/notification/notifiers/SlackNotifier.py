from notification.notifiers.Notifier import Notifier
from utils.Utils import isnone
import requests


class SlackNotifier(Notifier):
    """
    A notifier implementation which provides functionality to send message on **slack** channels.
    This class can perform following operations

    1. Add new channel URL
    2. Remove a channel URL
    3. Clear all channels
    4. Restore to default channel
    5. Change or set a new message
    6. Overrides ``notify`` method from ``Notifier`` which will be invoked by ``NotificationService``

    """

    def __init__(self, msg):
        """
        Creates an instance and use msg parameter to send a message to added channels

        Parameters
        ----------
        msg : str
                a message to be send, default 'Hello'. User can send formatted message.
                Please refer `Slack - Basic message formatting <https://api.slack.com/docs/message-formatting />`_

        """
        #self._channel_urls = {'dont-hear-just-listen': 'https://hooks.slack.com/services/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'}
        # self._channel_urls = {'com-bot': 'https://hooks.slack.com/services/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'}
        self._msg = msg

    def add_url(self, namekey: str, url: str):
        """
        Adds a channel URL to send a message on the slack channel

        Parameters
        ----------
        namekey : str
                  A URL identifier which can be use to remove
        url : str
              A slack channel URL

        Returns
        --------
        SlackNotifier
            instance of this object

        """
        self._channel_urls[namekey] = url
        return self

    def remove_url(self, namekey: str):
        """
        Removes channel URL associated with ``namekey``,
        returns ``None`` if key is not present.

        Parameters
        ----------
        namekey: str
                 URL identifier which should be removed

        Returns
        --------
        str
            removed/popped element, ``None`` otherwise

        """
        return self._channel_urls.pop(namekey, None)

    def set_msg(self, msg: None):
        """
        Sets a new message to be sent to a slack channel. If input ``msg`` is ``None``,
        it will not change message.

        Parameters
        ----------
        msg : str
              a new message.
              Please refer `Slack - Basic message formatting <https://api.slack.com/docs/message-formatting />`_

        Returns
        --------
        SlackNotifier
            instance of this object

        """
        if not isnone(msg):
            self._msg = msg
        return self

    def clear_channels(self):
        """
        Clears all channels in case user needs to stop sending messages to added channels.
        **Note:** Please call ``restore_default`` to set to default channel

        """
        self._channel_urls.clear()

    def restore_default(self):
        """
        In case user wants to restore to default channel, then this method first clears all channels and
        sets to default channel.

        Returns
        --------
        SlackNotifier
            current instance of slack notifier

        """
        self.clear_channels()
        #self._channel_urls = {
        #    'dont-hear-just-listen': 'https://hooks.slack.com/services/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'}
        return self

    def notify(self):
        """
        A custom implementation to send a message on ``slack`` channels

        """
        if isnone(self._msg):
            body = {'text': '<!here> We are all set to send message on a slack channel!!! :smile: '}
        elif isinstance(self._msg, dict):
            body = self._msg
        else:
            body = {'text': self._msg}

        for url in self._channel_urls.values():
            requests.post(url, json=body)

        return self

