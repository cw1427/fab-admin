"""
Created on 2019-5-15

@author: chenwen9
"""
from gevent import monkey
monkey.patch_all()
import os
from redis.sentinel import Sentinel, SentinelConnectionPool
from redis.client import Redis
from redis.exceptions import ConnectionError
import inspect
import redis
from gevent.queue import LifoQueue, Full, Empty
import threading


class BlockingSentinelConnectionPool(SentinelConnectionPool):

    def __init__(self, service_name, sentinel_manager, max_connections=100, timeout=60,
                  queue_class=LifoQueue, **kwargs):

        self.queue_class = queue_class
        self.timeout = timeout
        super(BlockingSentinelConnectionPool, self).__init__(service_name, sentinel_manager,
                                            max_connections=max_connections, **kwargs)

    def __repr__(self):
        return "%s<service=%s(%s)" % (
            type(self).__name__,
            self.service_name,
            self.is_master and 'master' or 'slave',
        )

    def reset(self):
        self.pid = os.getpid()
        self._check_lock = threading.Lock()
        # Create and fill up a thread safe queue with ``None`` values.
        self.pool = self.queue_class(self.max_connections)
        while True:
            try:
                self.pool.put_nowait(None)
            except Full:
                break
        # Keep a list of actual connection instances so that we can
        # disconnect them later.
        self._connections = []
        self.master_address = None
        self.slave_rr_counter = None

    def make_connection(self):
        "Make a fresh connection."
        connection = self.connection_class(**self.connection_kwargs)
        self._connections.append(connection)
        return connection

    def get_connection(self, command_name, *keys, **options):
        """
        Get a connection, blocking for ``self.timeout`` until a connection
        is available from the pool.

        If the connection returned is ``None`` then creates a new connection.
        Because we use a last-in first-out queue, the existing connections
        (having been returned to the pool after the initial ``None`` values
        were added) will be returned before ``None`` values. This means we only
        create new connections when we need to, i.e.: the actual number of
        connections will only increase in response to demand.
        """
        # Make sure we haven't changed process.
        self._checkpid()

        # Try and get a connection from the pool. If one isn't available within
        # self.timeout then raise a ``ConnectionError``.
        connection = None
        try:
            connection = self.pool.get(block=True, timeout=self.timeout)
        except Empty:
            # Note that this is not caught by the redis client and will be
            # raised unless handled by application code. If you want never to
            raise ConnectionError("No connection available.")

        # If the ``connection`` is actually ``None`` then that's a cue to make
        # a new connection to add to the pool.
        if connection is None:
            connection = self.make_connection()

        try:
            # ensure this connection is connected to Redis
            connection.connect()
            # connections that the pool provides should be ready to send
            # a command. if not, the connection was either returned to the
            # pool before all data has been read or the socket has been
            # closed. either way, reconnect and verify everything is good.
            if not connection.is_ready_for_command():
                connection.disconnect()
                connection.connect()
                if not connection.is_ready_for_command():
                    raise ConnectionError('Connection not ready')
        except:  # noqa: E722
            # release the connection back to the pool so that we don't leak it
            self.release(connection)
            raise

        return connection

    def release(self, connection):
        "Releases the connection back to the pool."
        # Make sure we haven't changed process.
        self._checkpid()
        if connection.pid != self.pid:
            return

        # Put the connection back into the pool.
        try:
            self.pool.put_nowait(connection)
        except Full:
            # perhaps the pool has been reset() after a fork? regardless,
            # we don't want this connection
            pass

    def disconnect(self):
        "Disconnects all connections in the pool."
        self._checkpid()
        for connection in self._connections:
            connection.disconnect()


class MySentinel(Sentinel):
    """
    self Sentinel class.
    """

    def slave_for(self, service_name, redis_class=Redis, connection_pool_obj=None,
                  connection_pool_class=SentinelConnectionPool, **kwargs):
        """
        overwrite slave_for to split the connection_kwargs to the redis_class.
        """
        kwargs['is_master'] = False
        connection_kwargs = dict(self.connection_kwargs)
        connection_kwargs.update(kwargs)
        # split the conection_kwargs parameter to the redis_class
        base_args = inspect.getargspec(redis.client.Redis.__init__).args
        base_args.append('is_master')
        base_args.append('check_connection')
        extra_kwargs = {key: connection_kwargs[key] for key in connection_kwargs.keys() if key not in base_args}
        base_kwargs = {key: connection_kwargs[key] for key in connection_kwargs.keys() if key in base_args}
        if connection_pool_obj:
            connection_pool_obj.is_master = base_kwargs.pop('is_master', True)
            connection_pool_obj.check_connection = base_kwargs.pop('check_connection', False)
            connection_pool_obj.connection_kwargs.update(base_kwargs)
            return redis_class(connection_pool=connection_pool_obj, **extra_kwargs)
        return redis_class(connection_pool=connection_pool_class(
            service_name, self, **base_kwargs), **extra_kwargs)

    def master_for(self, service_name, redis_class=Redis, connection_pool_obj=None,
                   connection_pool_class=SentinelConnectionPool, **kwargs):
        """
        overwrite master_for to setup the customize encoder.
        """
        kwargs['is_master'] = True
        connection_kwargs = dict(self.connection_kwargs)
        connection_kwargs.update(kwargs)
        # split the conection_kwargs parameter to the redis_class
        base_args = inspect.getargspec(redis.client.Redis.__init__).args
        base_args.append('is_master')
        base_args.append('check_connection')
        extra_kwargs = {key: connection_kwargs[key] for key in connection_kwargs.keys() if key not in base_args}
        base_kwargs = {key: connection_kwargs[key] for key in connection_kwargs.keys() if key in base_args}
        if connection_pool_obj:
            connection_pool_obj.is_master = base_kwargs.pop('is_master', True)
            connection_pool_obj.check_connection = base_kwargs.pop('check_connection', False)
            connection_pool_obj.connection_kwargs.update(base_kwargs)
            return redis_class(connection_pool=connection_pool_obj, **extra_kwargs)
        return redis_class(connection_pool=connection_pool_class(
            service_name, self, **base_kwargs), **extra_kwargs)
