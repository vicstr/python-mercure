# -*- coding: utf-8 -*-
"""
@author: Vitor Villar <vitor.luis98@gmail.com>
"""
from threading import Thread

import sseclient

from .message import Message


class Consumer(Thread):
    mercure_hub = None
    topics = None
    sse_client = None
    callback = None

    def __init__(self, mercure_hub, topics, callback, **request_kwargs):
        super().__init__()

        self.mercure_hub = mercure_hub
        self.topics = topics
        self.callback = callback
        self.request_kwargs = request_kwargs

    def start_consumption(self):
        """
        Consumes the message into a new thread
        :return:
        """
        self._build_client()
        self.start()

    def _build_client(self):
        """
        Build the SSEClient connection
        :return:
        """
        self.sse_client = sseclient.SSEClient(
            self.mercure_hub,
            params={'topic': self.topics},
            **self.request_kwargs
        )

    def run(self) -> None:
        """
        Start the event listening
        """
        for event in self.sse_client:
            # Create a new message object for each new income message
            msg = Message(
                self.topics,
                event.data,
                message_id=event.id,
                event_type=event.event
            )
            self.callback(msg)
