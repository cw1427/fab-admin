'''
Created on {* now *}
@desc: common sse module (server-side send event)
@app: {* app_name *}
'''
# coding=utf-8
from __future__ import unicode_literals

from collections import OrderedDict
from flask import Blueprint, request, current_app, json, stream_with_context, g, session
import six
import logging


__version__ = '0.2.1'

log = logging.getLogger(__name__)


@six.python_2_unicode_compatible
class Message(object):
    """
    Data that is published as a server-sent event.
    """
    def __init__(self, data, type=None, id=None, retry=None):
        """
        Create a server-sent event.

        :param data: The event data. If it is not a string, it will be
            serialized to JSON using the Flask application's
            :class:`~flask.json.JSONEncoder`.
        :param type: An optional event type.
        :param id: An optional event ID.
        :param retry: An optional integer, to specify the reconnect time for
            disconnected clients of this stream.
        """
        self.data = data
        self.type = type
        self.id = id
        self.retry = retry

    def to_dict(self):
        """
        Serialize this object to a minimal dictionary, for storing in Redis.
        """
        # data is required, all others are optional
        d = {"data": self.data}
        if self.type:
            d["type"] = self.type
        if self.id:
            d["id"] = self.id
        if self.retry:
            d["retry"] = self.retry
        return d

    def __str__(self):
        """
        Serialize this object to a string, according to the `server-sent events
        specification <https://www.w3.org/TR/eventsource/>`_.
        """
        if isinstance(self.data, six.string_types):
            data = self.data
        else:
            data = json.dumps(self.data)
        lines = ["data:{value}".format(value=line) for line in data.splitlines()]
        if self.type:
            lines.insert(0, "event:{value}".format(value=self.type))
        if self.id:
            lines.append("id:{value}".format(value=self.id))
        if self.retry:
            lines.append("retry:{value}".format(value=self.retry))
        return "\n".join(lines) + "\n\n"

    def __repr__(self):
        kwargs = OrderedDict()
        if self.type:
            kwargs["type"] = self.type
        if self.id:
            kwargs["id"] = self.id
        if self.retry:
            kwargs["retry"] = self.retry
        kwargs_repr = "".join(
            ", {key}={value!r}".format(key=key, value=value)
            for key, value in kwargs.items()
        )
        return "{classname}({data!r}{kwargs})".format(
            classname=self.__class__.__name__,
            data=self.data,
            kwargs=kwargs_repr,
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.data == other.data and
            self.type == other.type and
            self.id == other.id and
            self.retry == other.retry
        )


class ServerSentEventsBlueprint(object):
    """
    A :class:that knows how to publish, subscribe to,
    and stream server-sent events.
    """

    def __init__(self):
        pass

    @property
    def redis(self):
        """
        A :class:`redis.StrictRedis` instance, configured to connect to the
        current application's Redis server.
        """
        # change redis initiation from origin redis to sentinel for Redis HA.
        # redis_url = current_app.config.get("SSE_REDIS_URL")
        # if not redis_url:
        #    redis_url = current_app.config.get("REDIS_URL")
        # if not redis_url:
        #    raise KeyError("Must set a redis connection URL in app config.")
        # return StrictRedis.from_url(redis_url)
        sse_master = current_app.extensions['sse_master']
        return sse_master

    def publish(self, data, type=None, id=None, retry=None, channel='sse'):
        """
        Publish data as a server-sent event.

        :param data: The event data. If it is not a string, it will be
            serialized to JSON using the Flask application's
            :class:`~flask.json.JSONEncoder`.
        :param type: An optional event type.
        :param id: An optional event ID.
        :param retry: An optional integer, to specify the reconnect time for
            disconnected clients of this stream.
        :param channel: If you want to direct different events to different
            clients, you may specify a channel for this event to go to.
            Only clients listening to the same channel will receive this event.
            Defaults to "sse".
        """
        message = Message(data, type=type, id=id, retry=retry)
        msg_json = json.dumps(message.to_dict())
        return self.redis.publish(channel=channel, message=msg_json)

    def messages(self, channel):
        """
        A generator of :class:`~flask_sse.Message` objects from the given channel.
        """
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        try:
            for pubsub_message in pubsub.listen():
                if pubsub_message['type'] == 'message':
                    msg_dict = json.loads(pubsub_message['data'])
                    yield Message(**msg_dict)
        except GeneratorExit:
            pubsub.close()
        except Exception as e:
            log.error(e)

    def stream(self, channel=None):
        """
        A view function that streams server-sent events. Ignores any
        :mailheader:`Last-Event-ID` headers in the HTTP request.
        Use a "channel" query parameter to stream events from a different
        channel than the default channel (which is "sse").
        """
        if not channel:
            channel = request.values.get('channel') or 'sse'

        @stream_with_context
        def generator():
            try:
                for message in self.messages(channel=channel):
                    yield str(message)
            except GeneratorExit:
                pass

        return current_app.response_class(
            generator(),
            mimetype='text/event-stream',
            headers={'X-Accel-Buffering': 'no', 'chunked_transfer_encoding': 'off', 'Cache-Control': 'no-cache'}
        )

    def heart_beat(self, redis_client=None):
        # get current all sse related channels
        if redis_client:
            self.redis = redis_client
        channels = self.redis.pubsub_channels(pattern='sse*')
        for channel in channels:
            message = Message('ping', type='heartbeat')
            msg_json = json.dumps(message.to_dict())
            self.redis.publish(channel, message=msg_json)

sse = ServerSentEventsBlueprint()
